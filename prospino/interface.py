import argparse, subprocess, traceback, sys, json, textwrap
from shutil import copyfile

def main():
    args = parse_arg()
    slha = sys.stdin.readlines()

    try:
        r = xsec(args, slha)
        r['Error'] = False
    except Exception as e:
        r = {'Error' : True}
        _, _, tb = sys.exc_info()
        tb = ''.join(traceback.format_exception(e.__class__, e, tb))
        r['Traceback'] = tb

    print(json.dumps(r, sort_keys=True, indent=2))


def xsec(args, slha):
    workdir = '/prospino/'
    prospino = workdir + 'prospino_2.run'

    prospino_in = workdir + 'prospino.in.les_houches'
    dat  = workdir + 'prospino.dat'
    dat2 = workdir + 'prospino.dat2'
    dat3 = workdir + 'prospino.dat3'

    with open(prospino_in, 'w') as f:
        f.write(''.join(slha))

    arg_order =  ['inlo', 'isq_ng_in', 'icoll_in', 'energy_in', 'i_error_in', 'final_state_in', \
                  'ipart1_in', 'ipart2_in', 'isquark1_in', 'isquark2_in']
    command = [workdir+'prospino_2.run'] + [str(args[v]) for v in arg_order]

    try:
        o = subprocess.check_output(command, stderr=subprocess.STDOUT, cwd=workdir)
        print(o)
    except subprocess.CalledProcessError as e:
        raise Exception('prospino: ' + str(e) + ':\n' + e.output)

    return parse_prospino_output(dat, dat3)


def parse_prospino_output(dat, dat3):
    with open(dat, 'r') as f:
        s = f.readlines()
        l = s[0].split()

    r = {}

    r['CROSSLO']      = float(l[9])
    r['CROSSLOERR']   = float(l[10])
    r['CROSSNLO']     = float(l[11])
    r['CROSSNLOERR']  = float(l[12])
    r['KFACTOR'] = float(l[13])

    with open(dat3, 'r') as f:
        s = f.readlines()

    for n, l in enumerate(s):
        if 'm_gluino' in l:
            r['MGLUINO'] = float(l.split('=')[1])
        elif 'm_sdr' in l:
            r['MSQUARK'] = float(l.split('=')[1])
        elif 'm_char1' in l:
            r['MCHA1'] = float(l.split('=')[1])
        elif 'm_neut2' in l:
            r['MNEU2'] = float(l.split('=')[1])
        elif 'Z_bw' in l:
            r['N21'], r['N22'], r['N23'], r['N24'] = list(map(float, s[n+1].split()[:4]))
        elif 'U' in l:
            r['U11'], r['U12'] = list(map(float, l.split()[2:4]))
        elif 'V' in l:
            r['V11'], r['V12'] = list(map(float, l.split()[2:4]))

    return r


def parse_arg():
    a = argparse.ArgumentParser(prog='prospino',
                                description='Dockerized version of the prospino cross-section calculator.',
                                formatter_class=argparse.RawTextHelpFormatter)

    a.add_argument('--energy_in', type=int, required=True, help='Collider energy in GeV')

    final_states_choices = ['ng', 'ns', 'nn', 'll', 'sb', 'ss', 'tb', 'bb', 'gg', 'sg', 'lq', 'le']
    a.add_argument('--final_state_in', type=str, required=True, choices=final_states_choices,
                   help=textwrap.dedent('''\
                        Specify the final state
                         ng   neutralino/chargino + gluino
                         ns   neutralino/chargino + squark
                         nn   neutralino/chargino pair combinations
                         ll   slepton pair combinations
                         sb   squark-antisquark
                         ss   squark-squark
                         tb   stop-antistop
                         bb   sbottom-antisbottom
                         gg   gluino pair
                         sg   squark + gluino
                         lq   leptoquark pairs (using stop1 mass)
                        '''))

    a.add_argument('--ipart1_in', type=int, default=1, choices=range(14+1),
                   help=textwrap.dedent('''\
                   Details for non light-squark final states
                   final_state_in = ng,ns,nn
                   ipart1_in   = 1,2,3,4  neutralinos
                                 5,6      positive charge charginos
                                 7,8      negative charge charginos
                   ipart2_in the same
                   chargino+ and chargino- different processes

                   final_state_in = ll
                   ipart1_in   = 0        sel,sel + ser,ser  (first generation)
                                 1        sel,sel
                                 2        ser,ser
                                 3        snel,snel
                                 4        sel+,snl
                                 5        sel-,snl
                                 6        stau1,stau1
                                 7        stau2,stau2
                                 8        stau1,stau2
                                 9        sntau,sntau
                                 10        stau1+,sntau
                                 11        stau1-,sntau
                                 12        stau2+,sntau
                                 13        stau2-,sntau
                                 14        H+,H- in Drell-Yan channel

                    final_state_in = tb and bb
                    ipart1_in   = 1        stop1/sbottom1 pairs
                                  2        stop2/sbottom2 pairs

                    note: otherwise ipart1_in,ipart2_in have to set to 1 if not used
                    '''))

    a.add_argument('--ipart2_in', type=int, default=1, choices=range(14+1), help='See help for ipart1_in')
    a.add_argument('--inlo', type=int, default=1, choices=[0,1], help='LO only [0] or NLO [1]')
    a.add_argument('--isq_ng_in', type=int, default=1, choices=[0,1], help='Degenerate [0] or free [1] squark masses')
    a.add_argument('--icoll_in', type=int, default=1, choices=[0,1], help='Tevatron [0] or LHC [1]')
    a.add_argument('--i_error_in', type=int, default=0, choices=[0,1], help='Central scale [0] or scale variation [1]')

    a.add_argument('--isquark1_in', type=int, default=0, choices=range(-5,5+1),
                   help=textwrap.dedent('''\
                        For LO with light-squark flavor in the final state
                        isquark1_in     =  -5,-4,-3,-2,-1,+1,+2,+3,+4,+5
                                          (bL cL sL dL uL uR dR sR cR bR) in CteQ ordering
                        isquark1_in     = 0 sum over light-flavor squarks throughout
                        (the squark mass in the data files is then averaged)

                        flavors in initial state: only light-flavor partons, no bottoms
                        bottom partons only for Higgs channels
                        flavors in final state: light-flavor quarks summed over five flavors
                        '''))
    a.add_argument('--isquark2_in', type=int, default=0, choices=range(-5,5+1), help='See  help for isquark1_in')

    args = a.parse_args()
    return vars(args)

if __name__ == '__main__':
    main()

