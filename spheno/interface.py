import argparse, subprocess, traceback, sys, json, textwrap
from shutil import copyfile

def main():
    args = parse_arg()

    slha_in  = sys.stdin.readlines()
    slha_out = spheno(slha_in)

    print(''.join(slha_out))


def spheno(slha):
    workdir = '/spheno/'
    spheno = workdir + 'bin/SPheno'

    spheno_in  = workdir + 'LesHouches.in'
    spheno_out = workdir + 'SPheno.spc'

    with open(spheno_in, 'w') as f:
        f.write(''.join(slha))

    command = [spheno, spheno_in]

    try:
        o = subprocess.check_output(command, stderr=subprocess.STDOUT, cwd=workdir)
    except subprocess.CalledProcessError as e:
        raise Exception('spheno: ' + str(e) + ':\n' + e.output)

    with open(spheno_out, 'r') as f:
        slha_out = f.readlines()

    return slha_out


def parse_arg():
    a = argparse.ArgumentParser(prog='spheno',
                                description=textwrap.dedent('''\
                                  Dockerized version of SPheno SUSY spectrum calculator.

                                  Takes SLHA file as input and writes SLHA to output.
                                  '''),
                                formatter_class=argparse.RawTextHelpFormatter)

    args = a.parse_args()
    return vars(args)

if __name__ == '__main__':
    main()

