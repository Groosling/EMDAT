"""
UBC Eye Movement Data Analysis Toolkit (EMDAT), Version 3
Created on 2012-08-23

Sample code to run EMDAT for a given experiment (multiprocessing version).

@author: Sebastien Lalle (creator), Samad Kardan
Institution: The University of British Columbia.
"""

from multiprocessing import freeze_support, cpu_count
from BasicParticipant_multiprocessing import *
from EMDAT_core.Participant import export_features_all, write_features_tsv
from EMDAT_core.ValidityProcessing import output_Validity_info_Segments, output_percent_discarded, output_Validity_info_Participants
import sys

def loadRspFile():
    """ Load default pupil sizes of participants """
    with open('data/allData/pupilSizes.tsv', 'r') as tsv:
        pupilSizes = dict([line.strip().split('\t') for line in tsv])

        for key in pupilSizes:
            pupilSizes[key] = float(pupilSizes[key])
    return pupilSizes

if __name__ == '__main__':

    freeze_support() #for windows
    if len(sys.argv) < 2 :
        print ("No participants selected for feature extraction")
        exit(1)
    taskId = sys.argv[1]
    ul =  sys.argv[2:]
    uids = sys.argv[2:]

    alogoffset = [0] * len(sys.argv[2:])

    pupilSizes = loadRspFile()

    ###### Read participants
    nbprocess = 1
    ps = read_participants_Basic_multiprocessing(nbprocess, user_list = ul,pids = uids, log_time_offsets = alogoffset, datadir=params.EYELOGDATAFOLDER,
                               prune_length = None,
                               aoifile = "./data/allData/aois.aoi",
                               require_valid_segs = False, auto_partition_low_quality_segments = False,
                               rpsfile = None, taskId=taskId, pupilSizes=pupilSizes)

    ######

    if params.DEBUG or params.VERBOSE == "VERBOSE":
        #explore_validation_threshold_segments(ps, auto_partition_low_quality_segments = False)
        output_Validity_info_Segments(ps, auto_partition_low_quality_segments_flag = False, validity_method = 3)
        output_percent_discarded(ps,'./output/EMDAT/disc_multiprocessing.csv')
        output_Validity_info_Segments(ps, auto_partition_low_quality_segments_flag = False, validity_method = 2, threshold_gaps_list = [100, 200, 250, 300],output_file = "./output/EMDAT/Seg_val_multiprocessing.csv")
        output_Validity_info_Participants(ps, include_restored_samples =True, auto_partition_low_quality_segments_flag = False)


    ##### WRITE features to file
    print
    aoi_feat_names = (map(lambda x:x, params.aoigeneralfeat))
    print "Exporting features:\n--General:", params.featurelist, "\n--AOI:", aoi_feat_names, "\n--Sequences:", params.aoisequencefeat
    write_features_tsv(ps, './output/EMDAT/sample_features_multiprocessing.tsv',featurelist = params.featurelist, aoifeaturelist=aoi_feat_names, id_prefix = False)

    ##### WRITE AOI sequences to file
    write_features_tsv(ps, './output/EMDAT/sample_sequences_multiprocessing.tsv',featurelist = params.aoisequencefeat, aoifeaturelist=aoi_feat_names, id_prefix = False)

    #### Export pupil dilations for each scene to a separate file
    #print "--pupil dilation trends"
    #plot_pupil_dilation_all(ps, './outputfolder/pupilsizes/', "problem1")
    #plot_pupil_dilation_all(ps, './outputfolder/pupilsizes/', "problem2")
