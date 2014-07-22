#!/usr/bin/env python2

import os
import re
import vcf

from math import log10, floor, fabs, sqrt
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
from numpy import *
from pylab import *
from matplotlib.mlab import *
from copy import deepcopy

#from Parse.ParseVCF import MutRecord


class MutClusterRecord(object):
    """docstring for ClusterRecord"""
    def __init__(self,
                 chrom=None,
                 size=None,
                 start=None,
                 end=None,
                 mut_dist=[],
                 mut_pos=[],
                 mut_freq=[],
                 mut_filter=[],
                 mut_descr=[],
                 cluster_descr={}):
        #super(ClusterRecord, self).__init__()
        self.chrom = chrom
        self.size = size
        self.start = start
        self.end = end
        self.mut_dist = mut_dist
        self.mut_pos = mut_pos
        self.mut_freq = mut_freq
        self.mut_filter = mut_filter
        self.mut_descr = mut_descr
        self.len = self.end - self.start + 1
        self.descr = {}
        self.mean_dist = None
    #"#Chrom MutN Start End DistL PosL FilterL PosDescrL\n"   
    
    def get_mean_dist(self):
        self.mean_dist = sum(self.mut_dist)/len(self.mut_dist)    
        return self.mean_dist 

    def mcl_string(self):
        return "%s %i %i %i %s %s %s %s %s\n" % (self.chrom, self.size, self.start, self.end, 
                                                 self.mut_dist, self.mut_pos, self.mut_freq, 
                                                 self.mut_filter, self.mut_descr)


class Mutations(object):
    """docstring for MutationDict"""

    dictionary = {}
    mutdict = {}

    dictionary = {}
    metadata = {}
    merged_dict = {}
    not_SNPs = {}
    info = {}
    homozygotes = {}
    sorted_by_ref = {}

    mutpos_dict = {}
    mutdist_dict = {}

    cluster_dict = {}
    distance_dict = {}
    mutpos_descr_info = {}

    def __init__(self):
        #super(MutationDict, self).__init__()
        #self.arg = arg
        pass

    def make_dict_from_files(self, files_dict):
        pass

    def chrom(self):
        pass

    def merge_data(self):
        pass

    def find_not_SNPs(self, output="none"):
        pass

    def find_homozygotes(self):
        pass

    def find_by_reference(self, reference):
        pass

    def get_info(self):
        pass

    def mutation_map(self, mut_dict, filter_list, barfig="single", draw=False):
        pass

    def mutation_distance_distribution(self):
        pass

    def find_clusters(self, max_cluster_dist, filter_list=["All"]):
        pass

    def analyze_mut_pos(self, refgenome):
        pass

    def analyze_cluster_pos(self, min_length_filter=2, max_length_filter=100000, number_filter=2):
        pass                    


class MutationsVcf(Mutations):
    """docstring for MutationDictVcf"""
    
    allowed_filetypes = ["vcf"]
    figure_counter = 1

    def __init__(self, source, from_file=False):
        if from_file:
            self.source_filename = source
            self.metadata = vcf.Reader(open(source, 'r'))
            # vcf.Reader is ITERATOR and also stores metadata, requied for  writing vcf files
            # why so? All questions to the author of PyVCF.
            ######self.dictionary[file_entry] = [record for record in self.metadata[file_entry]]
            self.data = [record for record in self.metadata]
            #for mutrecord in self.mutdict[file_entry]:
            #    print mutrecord.chrom, mutrecord.pos, mutrecord.filters, mutrecord.samples
        else:
            #in this case source have to be tuple
            self.metadata = source[0]
            self.data = source[1]

    def __split_chromosomes(self):
        #TODO: check
        splited_dict = {}
        for record in self.data:
            if record.CHROM not in splited_dict:
                splited_dict[record.CHROM] = [record]
            else:
                splited_dict[record.CHROM].append(record)
        return splited_dict

    def filter_by_reference(self, reference_list):
        found_records = []
        filtered_out_records = []
        for record in self.data:
            if record.REF in reference_list:
                found_records.append(record)
            else:
                filtered_out_records.append(record)
        return MutationsVcf((self.metadata, found_records)), MutationsVcf((self.metadata, filtered_out_records))

    def filter_by_reference_and_alt(self, reference_alt_list):
        found_records = []
        filtered_out_records = []
        for record in self.data:
            #print (record.ALT)
            if (record.REF, record.ALT) in reference_alt_list:
                found_records.append(record)
            else:
                filtered_out_records.append(record)
        return MutationsVcf((self.metadata, found_records)), MutationsVcf((self.metadata, filtered_out_records))

    def write(self, out_filename):
        #vcf_writer = open(out_filename, 'w')
        vcf_writer = vcf.Writer(open(out_filename, 'w'), self.metadata)
        for record in self.data:
            vcf_writer.write_record(record)
        #vcf_writer.close()

    def __add__(self, other):
        print(self.metadata)
        print(other.metadata)

        pass
        return 1

    def __radd__(self, other):
        pass
        return 1

    """
    def merge_data(self):
        samples_list = []
        self.merged_dict = {"merged_file.vcf":[]}
        print ("\nMerging files:\n")
        for file_entry in self.dictionary:
            for s_entry in self.metadata[file_entry].samples:
                if s_entry not in samples_list:
                    samples_list.append(s_entry)
            print ("\t%s" % file_entry)
            for mut_record in self.dictionary[file_entry]:
                if not  self.merged_dict["merged_file.vcf"]:
                    self.merged_dict["merged_file.vcf"].append(mut_record)
                    continue
                append_pos = None
                doubled = 0
                for merged_record in self.merged_dict["merged_file.vcf"]:
                    if mut_record.chrom > merged_record.chrom:
                        continue
                    elif mut_record.chrom == merged_record.chrom:
                        #print "i" 
                        if mut_record.pos > merged_record.pos:
                            continue
                        elif mut_record.pos == merged_record.pos:
                            for samples_entry in mut_record.samples:
                                merged_record.samples.append(samples_entry)
                            doubled = 1
                            break 
                        if mut_record.pos < merged_record.pos:
                            append_pos = self.merged_dict["merged_file.vcf"].index(merged_record)
                            break
                    elif mut_record.chrom < merged_record.chrom:
                        append_pos = self.merged_dict["merged_file.vcf"].index(merged_record)
                        break

                if append_pos != None:
                    self.merged_dict["merged_file.vcf"].insert (append_pos, mut_record)
                else:
                    if not doubled:
                        self.merged_dict["merged_file.vcf"].append (mut_record)

        self.merged_dict_index = {}
        for file_entry in self.merged_dict:
            self.merged_dict_index[file_entry] = {}
            for record_number in xrange (len(self.merged_dict[file_entry])):
                if self.merged_dict[file_entry][record_number].chrom not in self.merged_dict_index[file_entry]:
                    self.merged_dict_index[file_entry][self.merged_dict[file_entry][record_number].chrom] = [record_number, None]

        self.chrom_number = len(self.merged_dict_index[file_entry])
        self.mut_number = len(self.merged_dict[file_entry])

        for chromosome in range (1, self.chrom_number +1 ):
            chrom_start = self.merged_dict_index[file_entry][str(chromosome)][0]
            if chrom_start!= 0:
                chrom_id = self.merged_dict[file_entry][chrom_start - 1].chrom
                self.merged_dict_index[file_entry][chrom_id][1] = chrom_start 

        self.merged_dict_index[file_entry][self.merged_dict[file_entry][self.mut_number - 1].chrom][1] = self.mut_number 
        print ("\nMerged file:")
        print ("\t Number of chromosomes: % i " % self.chrom_number)
        print ("\t Number of mutations: % i "%  self.mut_number)

        output_filename = "merged_file.vcf"
        vcf_writer = open(output_filename,'w')
        for record in self.merged_dict["merged_file.vcf"]:
            vcf_writer.write( "%s\t\t%s\t\t%s\t\t%s\t\t%s\n" % \
                        (record.chrom, record.pos, record.ref, record.alt,record.samples))        
        vcf_writer.close()
        """

    def find_not_SNPs(self, output="none"):
        """
        output option: "stdout" or "file" or "none" or "both"
        in any case not SNP mutations are stored in not_SNPs dict
        """
        """
        for file_entry in self.dictionary:
            self.not_SNPs[file_entry] = []
            for record in self.dictionary[file_entry]:
                if not record.is_snp:
                    self.not_SNPs[file_entry].append (record)
            if output == "file" or output == "both":
                output_filename = file_entry[:-4].split("/")[-1] + "_not_SNPs.vcf"
                vcf_writer = vcf.Writer(open(output_filename,'w'),self.metadata[file_entry])
                for record in self.not_SNPs[file_entry]:
                    vcf_writer.write_record(record)     
            if output == "stdout" or output =="both" :
                for record in self.not_SNPs[file_entry]:
                    print "%s\t\t%s\t\t%s\t\t%s\t\t%s" %\
                        (record.samples[0].sample, record.chrom, record.pos, record.ref, record.ALT)
        """
        for file_entry in self.dictionary:
            self.not_SNPs[file_entry] = []
            for mut_record in self.dictionary[file_entry]:
                if len(mut_record.ref) > 1:
                    self.not_SNPs[file_entry].append (mut_record)

            #writer
            """
            if output == "file" or output == "both":
                output_filename = file_entry[:-4].split("/")[-1] + "_not_SNPs.vcf"
                vcf_writer = vcf.Writer(open(output_filename,'w'),self.metadata[file_entry])
                for mut_record in self.not_SNPs[file_entry]:
                    vcf_writer.write_record(mut_record)
            """     
            if output == "stdout" or output =="both" :
                for mut_record in self.not_SNPs[file_entry]:
                    print ("%s\t\t%s\t\t%s\t\t%s\t\t%s" %\
                        (mut_record.samples[0].sample, mut_record.chrom, mut_record.pos, mut_record.ref, mut_record.alt))

    def find_homozygotes(self):
        #print "\nFormat of files %s.\n" % ftype
        for file_entry in self.dictionary:
            self.homozygotes[file_entry] = []
            for record in self.dictionary[file_entry]:
                for sample in record.samples:
                    gentype = sample.data.GT.split("|")
                    if gentype != [0,0] and gentype[0] == gentype[1]:
                        self.homozygotes[file_entry].append(record) 
                        print ("\t%s\t%s\t%s\t%s" % (sample.sample, record.chrom, record.pos , record.ref))

    def find_by_reference(self, reference):
        """
        reference - reference site (string)
        """
        found_mutations = {}
        for file_entry in self.dictionary:
            found_mutations[file_entry] = []
            for record in self.dictionary[file_entry]:
                if record.ref == reference:
                    found_mutations[file_entry].append (record)
        return found_mutations


    def get_info(self):
        self.info["Total"] = {                    \
                            "Totaly": 0,        \
                            "Reference" : {}    \
                            }
        for file_entry in self.dictionary:
            self.info[file_entry] = {            \
                                    "Totaly": 0,        \
                                    "Reference" : {}    \
                                    }
            self.info[file_entry]["Totaly"] = len(self.dictionary[file_entry])
            self.info["Total"]["Totaly"] += len(self.dictionary[file_entry])

            for record in self.dictionary[file_entry]:
                if record.ref not in self.info[file_entry]["Reference"]:
                    self.info[file_entry]["Reference"][record.ref]    = 1
                    if record.ref not in self.info["Total"]["Reference"]:
                        self.info["Total"]["Reference"][record.ref]    = 1
                    else:
                        self.info["Total"]["Reference"][record.ref]    += 1
                else :
                    self.info[file_entry]["Reference"][record.ref]    += 1
                    self.info["Total"]["Reference"][record.ref]    += 1

        info_file = open("general_info.info", "w")
        #print "\nFormat of files %s.\n" % ftype
        #info_file.write("Format of files %s.\n" % ftype)
        refsites_string = ""
        ref_keys = self.info["Total"]["Reference"].keys()
        ref_keys.sort()

        for reference in ref_keys:#self.info[ftype]["Total"]["Reference"]:
            refsites_string += "\t" + reference 
        print ("\tRefsites\t%s\tTotal\n" % refsites_string)
        info_file.write ("\tRefsites\t%s\tTotal\n" % refsites_string)
        file_entry_keys = self.info.keys()
        file_entry_keys.sort()
        for file_entry in file_entry_keys:
            if file_entry == "Total":
                continue
            number_string = ""
            for reference in ref_keys:#self.info[ftype]["Total"]["Reference"]:
                if reference not in self.info[file_entry]["Reference"]:
                    number_string += "\t%i" % 0 
                else:
                    number_string += "\t%i" % self.info[file_entry]["Reference"][reference]
            print ("\t%s\t%s\t%i " % (file_entry[:-4].split("/")[-1], number_string,self.info[file_entry]["Totaly"]))
            info_file.write ("\t%s\t%s\t%i\n " % (file_entry[:-4].split("/")[-1], number_string,self.info[file_entry]["Totaly"]))
        total_string = ""
        for reference in ref_keys:
            total_string += "\t%i" % self.info["Total"]["Reference"][reference]
                
        print ("\n\tTotal           " + total_string + "\t%i" % self.info["Total"]["Totaly"])
        info_file.write("\n\tTotal" + total_string + "\t%i\n" % self.info["Total"]["Totaly"])
        info_file.close()

    def calc_mut_freq(self, mut_dict):
        fd = open("mut_freq.info", "w")
        for file_entry in mut_dict:
            for record in mut_dict[file_entry]:
                record.calc_freq()
                fd.write("%s\t%s\t%i\n" % (record.chrom, record.pos, record.frequency))
        fd.close()

    def calc_mut_dist(self, mut_dict):
        handled_chromosomes = []
        fd = open("mut_dist.info", "w")
        for file_entry in mut_dict:
            for index in range(0, len(mut_dict[file_entry])):
                record = mut_dict[file_entry][index]
                if record.chrom not in handled_chromosomes:
                    record.distance = 0
                    handled_chromosomes.append(record.chrom)
                else:
                    record.distance = record.pos - mut_dict[file_entry][index-1].pos

                fd.write("%s\t%s\t%i\n" % (record.chrom, record.pos, record.distance))
        fd.close()

    def draw_mut_map (self, mut_dict = {}, ref_genome = None, min_gap_length = 10, single_fig = True, draw_gaps = False):
        if not mut_dict:
            mut_dict = self.merged_dict

        reference_color =   {
                            "A":0xFBFD2B, 
                            "C":0xFF000F,
                            "G":0x000FFF,
                            "T":0x4ED53F    
                            }
                            #A - yellow
                            #C - red
                            #G - blue
                            #T - green
        

        if ref_genome:
            if not ref_genome.gaps_dict:
                ref_genome.find_gaps()

        for file_entry in mut_dict:
            outputf = file_entry[:-4].split("/")[-1]
            chr_counter = 1
            data = {}
            """
            output_filename = "merged_file.vcf"
            vcf_writer = open(output_filename,'w')
            #print vcf_writer.metadata
            for record in mut_dict["merged_file.vcf"]:
                vcf_writer.write( "%s\t\t%s\t\t%s\t\t%s\t\t%s\n" % \
                                (record.chrom, record.pos, record.ref, record.alt,record.distance))        
            vcf_writer.close()"""

            for record in mut_dict[file_entry]:

                if record.chrom not in data:
                    index = 1
                    data[record.chrom] = {}
                    data[record.chrom][record.ref] = {record.frequency: [[index], [record.pos], [record.distance]]}
                else:
                    index += 1
                    if record.ref not in data[record.chrom]:
                        data[record.chrom][record.ref] = {}

                    if record.frequency not in data[record.chrom][record.ref]:
                        data[record.chrom][record.ref][record.frequency] = [[index], [record.pos], [record.distance]]
                    else:
                        data[record.chrom][record.ref][record.frequency][0].append(index)
                        data[record.chrom][record.ref][record.frequency][1].append(record.pos)
                        data[record.chrom][record.ref][record.frequency][2].append(record.distance)    
            #removing first mutation from the data set
            """    
            for chromosome in data:
                for frequency in data[chromosome]:
                    print chromosome, frequency
                    del(data[chromosome][frequency][0][0])
                    del(data[chromosome][frequency][1][0])
                    del(data[chromosome][frequency][2][0])"""

            if single_fig:
                figure(self.figure_counter,dpi = 150, figsize = (55, 70), facecolor = "#D6D6D6")
                self.figure_counter += 1
                sub_plot_list = []
            for chromosome in data:
                if single_fig:
                    print ( "Drawing  %s  of  %i chromosomes" % (chromosome,len(data)))
                        #figure(1,dpi = 100, figsize = (120, 128))
                    if len(sub_plot_list) >0:
                        sub_plot_list.append(subplot(len(data),1,chromosome, sharex = sub_plot_list[0], \
                                             sharey = sub_plot_list[0], axisbg = "#D6D6D6"))
                    else:
                        sub_plot_list.append(subplot(len(data),1,chromosome, axisbg = "#D6D6D6"))
                else:    
                    figure(self.figure_counter,dpi = 150, figsize = (6, 4), facecolor = "#D6D6D6")
                    self.figure_counter += 1
                    subplot(1,1, 1, axisbg = "#D6D6D6")
                for reference in data[chromosome]:
                    for frequency in data[chromosome][reference]:
                        frequency_color = reference_color[reference]
                    #    print 'color #%06x' % frequency_color
                        plot(data[chromosome][reference][frequency][1],data[chromosome][reference][frequency][2], color =  '#%06x' % frequency_color, \
                            marker = '.', linestyle  = 'None' ,label = 'Freq %i' % frequency)


                if ref_genome:
                    for gap in ref_genome.gaps_dict[chromosome]:
                        gca().add_patch(Rectangle((gap.location.start, 1),gap.location.end - gap.location.start, 1024*32,\
                                                 facecolor="#aaaaaa", edgecolor = 'none'))            

                title("Chromosome %s" % chromosome)     
                #xlabel("Position")
                ylabel("Distanse")
                ylim(ymin=1)
                axhline(y=100, color ="k")
                axhline(y=1000, color ="k")
                axhline(y=10, color ="k")
                try:
                    os.makedirs("rainplot/" + outputf)
                except OSError:
                    pass
                
                chr_counter += 1

                if not single_fig:
                    savefig("rainplot/" + outputf+"/"+ outputf +"_chr"+ chromosome + '.svg', facecolor = "#D6D6D6")

            if single_fig:
                savefig("rainplot/" + outputf+"/"+ outputf +"_all_chr"+'.svg', facecolor = "#D6D6D6")
                for sub_plot_entry in sub_plot_list:
                    sub_plot_entry.set_yscale('log',basey = 2)
                    yscale ('log', basey = 2)
                savefig("rainplot/" + outputf+"/"+ outputf +"_all_chr_log_scaled"+'.svg', facecolor = "#D6D6D6")
            
    def mututation_distance_distribution(self, mut_dict):
        distance_dict = {}
        log10_distance_dict = {}
        for file_entry in mut_dict:
            distance_dict[file_entry] = {}
            log10_distance_dict[file_entry] = {}
            for record  in mut_dict[file_entry]:
                if record.chrom not in distance_dict[file_entry]:
                    if record.distance != 0 :
                        distance_dict[file_entry][record.chrom] = [record.distance]
                        log10_distance_dict[file_entry][record.chrom] = [log10(record.distance)]
                else:
                    distance_dict[file_entry][record.chrom].append(record.distance)
                    log10_distance_dict[file_entry][record.chrom].append(log10(record.distance))
            figure(self.figure_counter,dpi = 70, figsize = (32, 24))
            self.figure_counter +=1
            for chromosome in distance_dict[file_entry]:
                subplot(4,4,chromosome)
                number_of_classes = 1 + floor(3.322*log10(len(distance_dict[file_entry][chromosome])))
                #print number_of_classes

                max_range = max(distance_dict[file_entry][chromosome])
                n, bins, patches = hist(distance_dict[file_entry][chromosome],range= (0,max_range),\
                                 bins =number_of_classes, label = "Distribution of distances between mutations.\nDistances longer the %i were ignored" % max_range)#ignoring dist longer then max_range bp
                #xscale('log')
                title("Chromosome %s" % chromosome,fontsize=12)     
                #xlabel("log(Distance)",fontsize=36)
                xlabel("Distance",fontsize=12)
                legend(fontsize = 12, loc ='upper center')
            savefig('mutation_distance_distribution.svg')

            figure(self.figure_counter,dpi = 70, figsize = (32, 24))
            self.figure_counter += 1
            for chromosome in log10_distance_dict[file_entry]:
                subplot(4,4,chromosome)
                number_of_classes = 1 + floor(3.322*log10(len(log10_distance_dict[file_entry][chromosome]))) 
                #print number_of_classes
                max_range = max(log10_distance_dict[file_entry][chromosome])
                mean_distance = sum(log10_distance_dict[file_entry][chromosome])/(len(log10_distance_dict[file_entry][chromosome]))
                deviation_list = [(dist10 - mean_distance)*(dist10 - mean_distance) for dist10 in log10_distance_dict[file_entry][chromosome]]
                stddev = sum(deviation_list)/len(deviation_list)

                n, bins, patches = hist(log10_distance_dict[file_entry][chromosome],range= (0,max_range),\
                                 bins =number_of_classes, label = "M %f \nSd %f" % (mean_distance, stddev))#ignoring dist longer then max_range bp
                bin_length = bins[2] - bins[1]
                bin_centers = [bin + (bin_length/2) for bin in bins]

                #print n

                gauss = normpdf(bin_centers , mean_distance, stddev)
                gauss *= bin_length
                #print sum(gauss)
                #print gauss
                gauss *=  len(log10_distance_dict[file_entry][chromosome])

                kolmogorov, kolmogorov_pred = self.kolmogorov_smirnov_test(n, gauss)
                #print gauss
                plot (bin_centers, gauss, 'r--', label = "Dmax = %f\nDst = %f" %(kolmogorov, kolmogorov_pred))
                #xscale('log')
                title("Chromosome %s" % chromosome,fontsize=12)     
                #xlabel("log(Distance)",fontsize=36)
                xlabel("Distance",fontsize=12)
                legend(fontsize = 12, loc ='upper left')
            savefig('mutation_distance_distribution_xlog.svg')

    def kolmogorov_smirnov_test(self, empirik_list, teoretical_list):
        cum_empirik_freq =[]
        cum_teoretical_freq = []
        for index in xrange(len(empirik_list)):
            ind = 0
            cum_empirik_freq.append(0)
            cum_teoretical_freq.append(0)
            while ind <= index:
                cum_empirik_freq[index] += empirik_list[ind]
                cum_teoretical_freq[index] += teoretical_list[ind]
                ind +=1
        difference = []
        for index in xrange(len(cum_empirik_freq)):        
            difference.append(fabs(cum_empirik_freq[index] - cum_teoretical_freq[index]))
        kolmogorov =     max(difference)/len(difference)
        kolmogorov_pred = 1.36/sqrt(len(difference))
        return     kolmogorov, kolmogorov_pred  

    def find_clusters(self,max_cluster_dist , mut_dict= {}):
        if not mut_dict:
            mut_dict = self.merged_dict

        self.max_cluster_dist = max_cluster_dist
        for file_entry in mut_dict:
            self.cluster_dict[file_entry] = []
            for chromosome in self.merged_dict_index[file_entry]:
                
                mut_in_cluster = 0
                cluster_start = 0
                cluster_end = 0
                dist_list = []
                pos_list = []
                freq_list = []
                cluster_filter_list = []
                pos_descr_list = []
                cluster = [mut_in_cluster, cluster_start, cluster_end,dist_list,pos_list, cluster_filter_list, pos_descr_list ]        
                mut_record_first = self.merged_dict_index[file_entry][chromosome][0]
                mut_record_last = self.merged_dict_index[file_entry][chromosome][1]        
                for mut_entry in range (mut_record_first+1, mut_record_last) :
                    mut_record  = mut_dict[file_entry][mut_entry]
                        #print set(mut[2]),set(mut[2]).difference(filter_list), filter_list
                    if (mut_record.distance <= max_cluster_dist):
                        if mut_in_cluster == 0:
                            cluster_start = mut_dict[file_entry][mut_entry-1].pos #prev_mut_position
                            mut_in_cluster +=1
                            pos_list.append(mut_dict[file_entry][mut_entry-1].pos)
                            freq_list.append(mut_dict[file_entry][mut_entry-1].frequency)
                            cluster_filter_list.append(mut_dict[file_entry][mut_entry-1].filter)
                            #pos_descr_list.append(mut_dict[file_entry][chromosome][mut_entry-1])
                        mut_in_cluster += 1
                        dist_list.append(mut_record.distance)
                        cluster_filter_list.append(mut_record.filter)
                        #pos_descr_list.append(mut[3])
                        pos_list.append(mut_record.pos)
                        freq_list.append(mut_record.frequency)
                    if (mut_record.distance > max_cluster_dist) and mut_in_cluster > 0:
                        cluster_end = mut_dict[file_entry][mut_entry-1].pos
                        if mut_in_cluster >2: #get clusters with three and more mutations
                            self.cluster_dict[file_entry].append(        \
                                        MutClusterRecord(chrom = chromosome, size = mut_in_cluster, start = cluster_start,\
                                        end = cluster_end, mut_dist = dist_list[:], mut_pos = pos_list[:], mut_freq = freq_list[:],\
                                        mut_filter = cluster_filter_list[:]) \
                                        )
                        mut_in_cluster = 0
                        dist_list = []
                        pos_list = []
                        cluster_filter_list = []
                        pos_descr_list = []
                        freq_list = []
        #    print "\n\t Found clusters:"
        #print "\n\t\tMaxMutDist\tChrom\ClustNumber"
        for file_entry in self.cluster_dict:
            cluster_filename = file_entry[:-4].split("/")[-1]
            cluster_file = open("%s_mutation_clusters_mcd_%i.mcl" % (cluster_filename, max_cluster_dist ), "w")
            cluster_file.write("#MaxMutDist %i\n" % self.max_cluster_dist)
            mcl_label_string = "#Chrom MutN Start End DistL PosL FreqL FilterL PosDescrL\n"
            cluster_file.write(mcl_label_string)
            for cluster in self.cluster_dict[file_entry]:
                mcl_record_string = cluster.mcl_string()
                #print mcl_record_string    
                cluster_file.write(mcl_record_string)
            cluster_file.close()                
            self.splited_clusters = self.__split_chromosomes(self.cluster_dict)

            figure(self.figure_counter,dpi = 70, figsize = (32, 24))
            self.figure_counter += 1

            for chromosome in self.splited_clusters[file_entry]:
                clust_len_list = []
                for cluster_record in self.splited_clusters[file_entry][chromosome]:
                    if cluster_record.size > 2:
                        clust_len_list.append(cluster_record.len)
                if     len(clust_len_list) < 2:
                    continue
                subplot(4,4,chromosome)
                number_of_classes = 1 + floor(3.322*log10(len(clust_len_list)))    

                len_hist = hist(clust_len_list,\
                                 bins =number_of_classes, label = "Distribution of cluster lengthes ")#ignoring dist longer then max_range bp
                title("Chromosome %s" % chromosome,fontsize=12)     
                xlabel("Cluster length",fontsize=12)
                #print chromosome
                #print len_hist 
            savefig ("cluster_length_dist_%i.svg" % max_cluster_dist)

            figure(self.figure_counter,dpi = 70, figsize = (32, 24))
            self.figure_counter += 1
            sub_plot_list = []
            for chromosome in self.splited_clusters[file_entry]:
                clust_size_list = []
                for cluster_record in self.splited_clusters[file_entry][chromosome]:
                    if cluster_record.size > 2:
                        clust_size_list.append(cluster_record.size)
                if     len(clust_size_list) < 2:
                    continue
                subplot(4,4,chromosome)
                if len(sub_plot_list) >0:
                    sub_plot_list.append(subplot(4,4,chromosome, sharex = sub_plot_list[0]))
                else:
                    sub_plot_list.append(subplot(4,4,chromosome))
                

    
                number_of_classes = 1 + floor(3.322*log10(len(clust_size_list)))
                hist(clust_size_list,\
                                 bins =max(clust_size_list), label = "Distribution of cluster lengthes ")#ignoring dist longer then max_range bp
                title("Chromosome %s" % chromosome,fontsize=12)     
                xlabel("Cluster size",fontsize=12)
            savefig ("cluster_size_dist_%i.svg" % max_cluster_dist)
        return self.splited_clusters
    
    def cluster_analysis(self, start_distance = 50 ,end_distance = 1500,step = 50, mut_dict= {}):
        if not mut_dict:
            mut_dict = self.merged_dict
        clusters = {}
        distance = start_distance
        while (distance <= end_distance):
            clusters[distance] = deepcopy(self.find_clusters(distance, mut_dict))
            distance +=step
        keys = clusters.keys()
        keys.sort()
        for file_entry in clusters[keys[0]]:
            for chromosome in clusters[keys[0]][file_entry]:
                for record in clusters[keys[0]][file_entry][chromosome]:
                    record.descr["new"] = keys[0]
        cluster_types_count = {}
        for index in range(1, len(keys)):
            cluster_types_count[keys[index]] = {}
            for file_entry in clusters[keys[index]]:
                cluster_types_count[keys[index]][file_entry] = {}
                for chromosome in clusters[keys[index]][file_entry]:
                    cluster_types_count[keys[index]][file_entry][chromosome] = {"new":0, \
                                                                                "merged": 0,\
                                                                                "extended": 0,\
                                                                                "no changes": 0,\
                                                                                "total": len(clusters[keys[index]][file_entry][chromosome])}
                    for cluster_record in clusters[keys[index]][file_entry][chromosome]:
                        #print keys[index]
                        #print cluster_record.chrom 
                        #print cluster_record.start 
                        #print cluster_record.end
                        #print cluster_record.descr
                        for prev_cluster_record in clusters[keys[index-1]][file_entry][chromosome]:
                            if prev_cluster_record.end < cluster_record.start:
                                continue
                            elif prev_cluster_record.start > cluster_record.end:
                                break
                            elif prev_cluster_record.start >= cluster_record.start and prev_cluster_record.end <= cluster_record.end:
                                if prev_cluster_record.start == cluster_record.start and prev_cluster_record.end == cluster_record.end:
                                    cluster_record.descr["left"] = "no changes"
                                    cluster_record.descr["right"] = "no changes"
                                    #print cluster_record.descr
                                    break    
                                if "contains" not in cluster_record.descr:
                                    cluster_record.descr["contains"] = [(prev_cluster_record.start, prev_cluster_record.end)]
                                    #print cluster_record.descr
                                else :
                                    cluster_record.descr["contains"].append((prev_cluster_record.start, prev_cluster_record.end))
                                    #print cluster_record.descr

                                if prev_cluster_record.start > cluster_record.start and prev_cluster_record.end == cluster_record.end:
                                    cluster_record.descr["left"] = "extened"
                                    cluster_record.descr["right"] = "no changes"
                                    break
                                if prev_cluster_record.start > cluster_record.start and prev_cluster_record.end < cluster_record.end:
                                    cluster_record.descr["left"] = "extened"
                                    cluster_record.descr["right"] = "extended"    
                                if prev_cluster_record.start == cluster_record.start and prev_cluster_record.end < cluster_record.end:
                                    cluster_record.descr["left"] = "no changes"
                                    cluster_record.descr["right"] = "extended"

                        #print cluster_record.descr
                        if  cluster_record.descr == {}:
                            cluster_record.descr["new"] = keys[index]
                            cluster_types_count[keys[index]][file_entry][chromosome]["new"] += 1
                            continue
                    #    print keys[index]
                    #    print cluster_record.descr
                        if cluster_record.descr["left"] == "no changes" and cluster_record.descr["right"] == "no changes":
                            cluster_types_count[keys[index]][file_entry][chromosome]["no changes"] += 1
                            continue
                        if len(cluster_record.descr["contains"]) > 1 :
                            cluster_types_count[keys[index]][file_entry][chromosome]["merged"] += 1
                        elif cluster_record.descr["left"] == "extended" or cluster_record.descr["right"] == "extended":
                            cluster_types_count[keys[index]][file_entry][chromosome]["extended"] += 1

        #print     cluster_types_count
        data = {}
        for index in range(1, len(keys)):
            for file_entry in cluster_types_count[keys[index]]:
                for chromosome in cluster_types_count[keys[index]][file_entry]:
                    if chromosome not in data:
                        data[chromosome] = [[],[],[],[],[],[]] 
                    data[chromosome][0].append(keys[index])    
                    data[chromosome][1].append(cluster_types_count[keys[index]][file_entry][chromosome]["new"])
                    data[chromosome][2].append(cluster_types_count[keys[index]][file_entry][chromosome]["no changes"])
                    data[chromosome][3].append(cluster_types_count[keys[index]][file_entry][chromosome]["extended"])
                    data[chromosome][4].append(cluster_types_count[keys[index]][file_entry][chromosome]["merged"])
                    data[chromosome][5].append(cluster_types_count[keys[index]][file_entry][chromosome]["total"])
                    """
                    data[chromosome].append ([keys[index],cluster_types_count[keys[index]][file_entry][chromosome]["new"],\
                                                          cluster_types_count[keys[index]][file_entry][chromosome]["no changes"],\
                                                          cluster_types_count[keys[index]][file_entry][chromosome]["extended"],\
                                                          cluster_types_count[keys[index]][file_entry][chromosome]["merged"]\
                                            ] )"""
                    #cluster_types_count[keys[index]][file_entry][chromosome] 
        for chromosome  in data:
            print (chromosome)
            for entry in data[chromosome]:
                print (entry)

        figure(self.figure_counter,dpi = 70, figsize = (32, 24))
        self.figure_counter += 1    
        sub_plot_list = []                
        for chromosome in data:
            subplot(4,4,chromosome)
            """
            if len(sub_plot_list) >0:
                sub_plot_list.append(subplot(4,4,chromosome, sharey = sub_plot_list[0]))
            else:
                sub_plot_list.append(subplot(4,4,chromosome))
            """
            plot (data[chromosome][0], data[chromosome][1], "r.-",\
                data[chromosome][0], data[chromosome][2], "g.-",\
                data[chromosome][0], data[chromosome][3], "b.-",\
                data[chromosome][0], data[chromosome][4], "k.-",\
                data[chromosome][0], data[chromosome][5], "c.-" \
                )    
            title("Chromosome %s" % chromosome,fontsize=12)     
            xlabel("Max distance between mutations",fontsize=12)
        savefig ("cluster_analysis.svg")
        """
                            elif prev_cluster_record.start == cluster_record.start and prev_cluster_record.end == cluster_record.end:
                                cluster_record.descr["left"] = "no changes"
                                cluster_record.descr["right"] = "no changes"
                                break
                            elif prev_cluster_record.start > cluster_record.start and prev_cluster_record.end == cluster_record.end:
                                cluster_record.descr["left"] = "extened"
                                cluster_record.descr["right"] = "no changes"
                                break
                            elif prev_cluster_record.start > cluster_record.start and prev_cluster_record.end < cluster_record.end:
                                cluster_record.descr["left"] = "extened"
                                cluster_record.descr["right"] = "extended"    
                            elif prev_cluster_record.start == cluster_record.start and prev_cluster_record.end < cluster_record.end:
                                cluster_record.descr["left"] = "no changes"
                                cluster_record.descr["right"] = "extended"
                                """
    """
    def analyze_mut_pos(self, refgenome):

        for file_entry in self.mutpos_dict:    
            self.mutpos_descr_info[file_entry] ={}
            for chromosome in self.mutpos_dict[file_entry]:
                self.mutpos_descr_info[file_entry][chromosome] = {}
                #print chromosome, len(self.mutpos_dict[file_entry][chromosome])
                for entry in self.mutpos_dict[file_entry][chromosome]:
                    entry_described = 0 
                    for feature in refgenome.feature_dict[chromosome]:
                        if entry[0] >= feature[1][0] and entry[0] <= feature[1][1]:
                            entry[3].append(feature)
                            entry_described = 1
                            if feature[0] not in  self.mutpos_descr_info[file_entry][chromosome]:
                                self.mutpos_descr_info[file_entry][chromosome][feature[0]] =1 
                            else:
                                self.mutpos_descr_info[file_entry][chromosome][feature[0]] +=1 
                    if entry_described == 0:
                        entry[3].append(["intergenic",[None,None],None])
                        if "intergenic" not in self.mutpos_descr_info[file_entry][chromosome]:
                            self.mutpos_descr_info[file_entry][chromosome]["intergenic"] =1
                        else:
                            self.mutpos_descr_info[file_entry][chromosome]["intergenic"] +=1
                                    #print entry

        for file_entry in self.mutpos_descr_info:
            #self.distance_dict[file_entry] = {}
            print "figure"
            figure(4,dpi = 70, figsize = (24, 24))
            for chromosome in self.mutpos_descr_info[file_entry]:
                #self.distance_dict[file_entry][chromosome] = []
                #for mut_entry in range (1, len(self.mutpos_dict[file_entry][chromosome])) :
                #    mut = self.mutpos_dict[file_entry][chromosome][mut_entry]
                    #self.distance_dict[file_entry][chromosome].append(log10(mut[1]))
                #    self.distance_dict[file_entry][chromosome].append(mut[1])
                subplot(4,4,chromosome)
                #number_of_classes = 1 + floor(3.322*log10(len(self.distance_dict[file_entry][chromosome])))
                #print number_of_classes
                #max_range = max(self.distance_dict[file_entry][chromosome])
                labels = self.mutpos_descr_info[file_entry][chromosome].keys()
                labels.sort()
                data = [self.mutpos_descr_info[file_entry][chromosome][key] for key in labels]
                additional_labels = [" (%i)" % self.mutpos_descr_info[file_entry][chromosome][key] for key in labels]
                colors_dict = {
                              "mRNA": "b",\
                              "intergenic" : "r",\
                              "tRNA" : "gold",\
                              "LTR" : "yellowgreen", \
                              "STS" : "c", \
                              "ncRNA" :  "green",\
                              "repeat_region": "m"\
                                      }
                full_labels = [] 
                for index in xrange(len(additional_labels)):
                    full_labels.append (labels[index]+ additional_labels[index])
                colors = [colors_dict[key] for key in labels ]
                pie(data, labels=full_labels, colors = colors,autopct='%1.1f%%',shadow=True)
            #    hist(self.distance_dict[file_entry][chromosome],range= (0,max_range),\
            #                             bins =number_of_classes, label = "Distribution of distances between mutations.\nDistances longer the %i were ignored" % max_range)#ignoring dist longer then max_range bp
                #xscale('log')
                title("Chromosome %s" % chromosome,fontsize=18)     
                #xlabel("log(Distance)",fontsize=36)
            #    xlabel("Distance",fontsize=12)
            #    legend(fontsize = 12, loc ='upper center')
        savefig('mutpos_descr_info.svg')

    def analyze_cluster_pos(self, min_length_filter = 2, max_length_filter = 100000, number_filter = 2):
        cluster_descr = {}
        for file_entry in self.cluster_dict:
            cluster_descr[file_entry] = {}
            for chromosome in self.cluster_dict[file_entry]:    
                cluster_descr[file_entry][chromosome] = {}
                for cluster in     self.cluster_dict[file_entry][chromosome]:
                    #print cluster
                    cluster_length = cluster[2] - cluster[1]
                    if cluster[0] >= number_filter and cluster_length >= min_length_filter and cluster_length <= max_length_filter:
                        feature_types = []
                        for feature in cluster[6]:
                            feature_types.append(feature[0][0])
                        feature_kinds = [fet for fet in set(feature_types)]
                        feature_kinds.sort()
                        feature_kinds.reverse()
                        combo_feature = ""
                        for feature in feature_kinds:
                            combo_feature +="/" + feature
                        combo_feature =  combo_feature[1:]
                        if combo_feature not in cluster_descr[file_entry][chromosome]:
                            cluster_descr[file_entry][chromosome][combo_feature] = 1
                        else:
                            cluster_descr[file_entry][chromosome][combo_feature] += 1
                         #print combo_feature

        for file_entry in cluster_descr:
            #self.distance_dict[file_entry] = {}
            figure(5,dpi = 70, figsize = (32, 32))
            for chromosome in cluster_descr[file_entry]:
                #self.distance_dict[file_entry][chromosome] = []
                #for mut_entry in range (1, len(self.mutpos_dict[file_entry][chromosome])) :
                #mut = self.mutpos_dict[file_entry][chromosome][mut_entry]
                #self.distance_dict[file_entry][chromosome].append(log10(mut[1]))
                #self.distance_dict[file_entry][chromosome].append(mut[1])
                subplot(4,4,chromosome)
                #number_of_classes = 1 + floor(3.322*log10(len(self.distance_dict[file_entry][chromosome])))
                #print number_of_classes
                #max_range = max(self.distance_dict[file_entry][chromosome])
                labels = cluster_descr[file_entry][chromosome].keys()
                labels.sort()
                data = [cluster_descr[file_entry][chromosome][key] for key in labels]
                additional_labels = [" (%i)" % cluster_descr[file_entry][chromosome][key] for key in labels]
                colors_dict = {
                                      "mRNA": "b",\
                                      "mRNA/intergenic": "b", \
                                      "mRNA/LTR": "b", \
                                      "intergenic" : "r",\
                                      "intergenic/LTR" : "r",\
                                      "intergenic/STS" : "r",\
                                      "tRNA" : "gold",\
                                      "tRNA/LTR" : "gold",\
                                      "tRNA/ncRNA/intergenic" : "gold",\
                                      "tRNA/intergenic" : "gold", \
                                      "tRNA/intergenic/STS" : "gold", \
                                      "tRNA/mRNA/intergenic" : "gold", \
                                      "tRNA/mRNA" : "gold", \
                                      "LTR" : "yellowgreen", \
                                      "LTR/intergenic" : "yellowgreen", \
                                      "STS" : "c", \
                                      "STS/intergenic" : "c", \
                                      "ncRNA" :  "green",\
                                      "ncRNA/mRNA" :  "green",\
                                      "ncRNA/mRNA/intergenic" :  "green",\
                                      "ncRNA/intergenic/LTR" :  "green",\
                                      "ncRNA/intergenic" :  "green",\
                                      "ncRNA/mRNA/intergenic/LTR" :  "green",\
                                      "repeat_region": "m"\
                              }
                full_labels = [] 
                for index in xrange(len(additional_labels)):
                    full_labels.append (labels[index]+ additional_labels[index])
                colors = [colors_dict[key] for key in labels ]
                pie(data, labels=full_labels, colors = colors, autopct='%1.1f%%',shadow=True) # colors = colors
            #    hist(self.distance_dict[file_entry][chromosome],range= (0,max_range),\
            #                             bins =number_of_classes, label = "Distribution of distances between mutations.\nDistances longer the %i were ignored" % max_range)#ignoring dist longer then max_range bp
                #xscale('log')
                title("Chromosome %s" % chromosome,fontsize=18)     
                #xlabel("log(Distance)",fontsize=36)
            #    xlabel("Distance",fontsize=12)
            #    legend(fontsize = 12, loc ='upper center')
        savefig('clusterpos_descr_info.svg')                        
    """

class ReferenceGenome(object):
    """docstring for ReferenceGenome"""
    chr_dict = {
                "chrI":"1",\
                "chrII":"2",\
                "chrIII":"3",\
                "chrIV":"4",\
                "chrV":"5",\
                "chrVI":"6",\
                "chrVII":"7",\
                "chrVIII":"8",\
                "chrIX":"9",\
                "chrX":"10",\
                "chrXI":"11",\
                "chrXII":"12",\
                "chrXIII":"13",\
                "chrXIV":"14",\
                "chrXV":"15",\
                "chrXVI":"16",\
                }
    feature_dict = {}
    gaps_dict = {}
    def __init__(self, ref_gen_file):
        #super(ReferenceGenome, self).__init__()
        #self#.arg = arg
        self.ref_gen_file = ref_gen_file
        self.reference_genome = SeqIO.index_db("refgen.idx", [ref_gen_file],"genbank")
        for entry in  self.reference_genome:
            entry_name = self.chr_dict[self.reference_genome[entry].description.split(" ")[1]]
            self.feature_dict[entry_name] = []
            for feature in self.reference_genome[entry].features:
                if not (feature.type == "CDS" or feature.type == "source" or feature.type == "gene" or\
                        feature.type =="rep_origin" or feature.type =="misc_feature"):
                    self.feature_dict[entry_name].append([feature.type, \
                                                    [feature.location.start,feature.location.end, feature.location.strand],\
                                                     feature.strand])
                #print feature.type,feature.location.start,feature.location.end, feature.location.strand
    def find_gaps (self):
        gap_reg_exp = re.compile("N+", re.IGNORECASE)
        for entry in  self.reference_genome:
            entry_name = self.chr_dict[self.reference_genome[entry].description.split(" ")[1]]
            self.gaps_dict[entry_name] = []
            #print self.reference_genome[entry].seq
            gaps = gap_reg_exp.finditer(str(self.reference_genome[entry].seq)) # iterator with 
            for match in gaps:
                self.gaps_dict[entry_name].append(     \
                                SeqFeature(FeatureLocation(match.start(), match.end()), type = "gap",strand = None )    \
                                )