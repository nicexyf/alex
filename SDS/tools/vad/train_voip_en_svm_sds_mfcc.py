#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from sklearn import *
from multiprocessing import *

import __init__

from SDS.utils.htk import *

max_files = 1000 # 4000
max_frames_per_segment = 1000

def save_svc(svc, file_name):
  f = open(file_name, 'w+')
  pickle.dump(svc, f)
  f.close()

def load_mlf(train_data_sil_aligned, max_files, max_frames_per_segment):
  mlf_sil = MLF(train_data_sil_aligned, max_files = max_files)
  mlf_sil.filter_zero_segments()
  # map all sp, _noise_, _laugh_, _inhale_ to sil
  mlf_sil.sub('sp', 'sil')
  mlf_sil.sub('_noise_', 'sil')
  mlf_sil.sub('_laugh_', 'sil')
  mlf_sil.sub('_inhale_', 'sil')
  # map everything except of sil to speech
  mlf_sil.sub('sil', 'speech', False)
  mlf_sil.merge()
  #mlf_sil.times_to_seconds()
  mlf_sil.times_to_frames()
  mlf_sil.trim_segments(30)
  mlf_sil.shorten_segments(max_frames_per_segment)

  return mlf_sil


train_data_sil = 'data_vad_sil/data/*.wav'
train_data_sil_aligned = 'data_vad_sil/vad-silence.mlf'

train_data_speech = 'data_voip_en/train/*.wav'
train_data_speech_aligned = 'asr_model_voip_en/aligned_best.mlf'

mlf_sil = load_mlf(train_data_sil_aligned, max_files, max_frames_per_segment)
mlf_speech = load_mlf(train_data_speech_aligned, max_files, max_frames_per_segment)

print datetime.datetime.now()
print "The length of sil segments in sil:    ", mlf_sil.count_length('sil')
print "The length of speech segments in sil: ", mlf_sil.count_length('speech')
print "The length of sil segments in speech:    ", mlf_speech.count_length('sil')
print "The length of speech segments in speech: ", mlf_speech.count_length('speech')

vta = MLFMFCCOnlineAlignedArray(usec0 = False)
vta.append_mlf(mlf_sil)
vta.append_trn(train_data_sil)
vta.append_mlf(mlf_speech)
vta.append_trn(train_data_speech)

X = [ h for h, l in vta]
y = [ 1 if l == 'speech' else 0 for h, l in vta]

X_1 = X[:len(X)/2]
y_1 = y[:len(X)/2]
X_2 = X[len(X)/2:]
y_2 = y[len(X)/2:]

print '-'*120
print 'VAD SVM training'
print datetime.datetime.now()
print '-'*120

#svc_vad1 = svm.SVC(cache_size=1000,C=1,gamma=.0005,kernel='rbf')
svc_vad1 = svm.NuSVC(cache_size=1000,nu=0.1,gamma=.0005, kernel='rbf')
svc_vad1.fit(X_1,y_1)
print "#support vectors", svc_vad1.n_support_

#svc_vad2 = svm.SVC(cache_size=1000,C=1,gamma=.0005,kernel='rbf')
svc_vad2 = svm.NuSVC(cache_size=1000,nu=0.1,gamma=.0005, kernel='rbf')
svc_vad2.fit(X_2,y_2)
print "#support vectors", svc_vad2.n_support_

save_svc(svc_vad1, 'model_voip_en/vad_sds_mfcc.svc')

print '-'*120
print 'VAD GMM test'
print datetime.datetime.now()
print '-'*120

accuracy = (svc_vad1.score(X_2,y_2) + svc_vad2.score(X_1,y_1))/2*100

print "VAD accuracy : %0.3f%% " % accuracy
print datetime.datetime.now()
