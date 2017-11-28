import os, sys
import argparse
import subprocess

import logging
from smp_base.common import get_module_logger
logger = get_module_logger(modulename = 'smp_data_check', loglevel = logging.DEBUG)

datafiles = {
    'sin_sweep_0-6.4Hz_newB.pickle': {'md5': '16da961befff74e296a3743d0ff76d7f'}
}

def main(args):
    # print "args.data_root", args.data_root

    do_data_root = False
    do_data_dir = False
    do_fetch = False
    
    if os.path.exists(args.data_root):
        logger.info('Data root at %s exists, checking for data iself', args.data_root)
        data_dir = '{0}/{1}'.format(args.data_root, 'data')
        if os.path.exists(data_dir):
            logger.info('Data directory at %s exists, checking for subdirs', data_dir)
            for d_ in os.walk(data_dir):
                if d_[0] != data_dir: continue
                logger.info('scanning dir entry %s', d_[0], )

                # check files
                if len(d_[2]) > 0:
                    logger.info('    found %d files to check', len(d_[2]))
                    # for sf_ in d_[2]:
                    #     logger.info('       file %s', sf_, )
                    datafiles_ = [df for df in datafiles if df in d_[2]]
                    if len(datafiles_) > 0:
                        logger.info('    found %d of %d datafiles, checking md5 sums', len(datafiles_), len(datafiles))
                        for df_ in datafiles_:
                            try:
                                df_md5 = subprocess.check_output(['md5sum', '{0}/{1}'.format(data_dir, df_)]).split(' ')[0]
                            except Exception, e:
                                logger.debug('datafile md5sum failed with %s', e)
                            if df_md5 != datafiles[df_]['md5']:
                                logger.error('Datafile md5 sums do not match %s != %s', df_md5, datafiles[df_]['md5'])
                                do_fetch = True
                            logger.info('        md5 OK')
                    else:
                        do_fetch = True
                else:
                    do_fetch = True
                    
                # # check subdirs
                # if len(d_[1]) > 0:
                #     logger.info('    found %d subdirs', len(d_[1]))
                #     for sd_ in d_[1]:
                #         logger.info('       subdir %s', sd_, )
                    
        else:
            do_data_dir = True
    else:
        do_data_root = True
        
    if do_data_root:
        # mkdir root
        pass
        
if __name__ == '__main__':
    defaults = {
        'data_root': '../smp_graphs/experiments'
    }
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data-root', type = str, default = defaults['data_root'], help = 'Parent directory where data is going to live [%s]' % (defaults['data_root']))

    args = parser.parse_args()

    main(args)
