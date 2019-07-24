import os
from examples.pytracker import PyTracker
from lib.utils import get_ground_truthes, plot_precision, plot_success
from examples.otbdataset_config import OTBDatasetConfig
import numpy as np

if __name__ == '__main__':
    dataset = "example"
    data_dir = '/root/simple_hao/dataset/{}'.format(dataset)
    data_names = sorted(os.listdir(data_dir))
    if "OTB100.json" in data_names:
        data_names.remove("OTB100.json")
    dataset_config = OTBDatasetConfig()
    # tracker_types = ['KCF_GRAY','Staple-CA', 'LDES','BACF', "DAT", "STRCF", "CN", 'SAMF', 'DSST',
    #                  'DSST-LP', 'CSK', 'MOSSE', 'KCF_CN', 'KCF_HOG', 'DCF_GRAY', 'DCF_HOG', 'MKCFup',
    #                  'MKCFup-LP','MCCTH-Staple','ECO','ECO-HC','CSRDCF','CSRDCF-LP', 'Staple']
    tracker_types = ["BACF"]
    np.set_printoptions(precision=3)

    for tracker_type in tracker_types:
        fpss=apses=psrs=fmaxs=aucs=precisions=[]
        for data_name in data_names:
            data_path = os.path.join(data_dir, data_name)
            gts = get_ground_truthes(data_path)
            if data_name in dataset_config.frames.keys():
                start_frame, end_frame = dataset_config.frames[data_name][:2]
                if data_name != 'David':
                    gts = gts[start_frame - 1:end_frame]
            img_dir = os.path.join(data_path, 'img')
            tracker = PyTracker(img_dir, tracker_type=tracker_type, dataset_config=dataset_config)
            result_path = "../results/CF/{0}/{1}/{2}".format(tracker_type, dataset, data_name)
            if not os.path.exists(result_path):
                os.makedirs(result_path)
            poses, fps, apce, psr, fmax  = tracker.tracking(verbose=True,
                                     video_path=os.path.join(result_path, data_name + '.avi'))
            auc = plot_success(gts, poses, os.path.join(result_path,  data_name+'_success.jpg'))
            precision = plot_precision(gts, poses, os.path.join(result_path,  data_name + '_precision.jpg'))

            fpss.append(np.float(fps))
            apses.append(np.float(apce))
            psrs.append(np.float(psr))
            fmaxs.append(np.float(fmax))
            aucs.append(np.float(auc))
            precisions.append(np.float(precision))

            file_path = "../results/CF/{0}/{1}/result.txt".format(tracker_type, dataset)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("Name\t\tFPS\t\tAPCE\t\tPSR\t\tFmax\t\tAUC\t\tPrecision\n")
                    f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(data_name, fps, apce, psr, fmax, auc, precision))
            else:
                with open(file_path, "a") as f:
                    f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(data_name, fps, apce, psr, fmax, auc, precision))

        with open(file_path, "a") as f:
            f.write("Average\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(str(np.mean(fpss))[:5], str(np.mean(apses))[:5], str(np.mean(psrs))[:5], str(np.mean(fmaxs))[:5], str(np.mean(aucs))[:5], str(np.mean(precisions))[:5]))
