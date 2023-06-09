# SAM Fileref: https://samtools.github.io/hts-specs/SAMv1.pdf
# Resource: DeBrujin: 
# https://eaton-lab.org/slides/genomics/answers/nb-10.2-de-Bruijn.html
from DeBruijn import *
from Alignment import Alignment
from tests import *
from file_tools import *
from processing_plot import *
import configparser

#
# Current primary function to process data

def process_data():
    config = configparser.ConfigParser()
    config.read('config.ini')

    files = get_files(str(config['DEFAULT']['data_path']))
    for file in files:
        print(file)
        with open(file, 'r') as infile:
            loopCount = 0
            lineCount = 0

            for line in infile:
                match lineCount:
                    case -1:
                        break  # Avoid reading the whole file, for now

                    case _:
                        entry = line.split("\t")
                        if not is_header(entry):
                            alignment = Alignment(entry)

                            #This should be unnecessary due to preprocessing
                            if alignment.IS_MAPPED and int(alignment.MAP_QUALITY) <= 15:  # Prints mapped entries
                 
                                #Find overlapping sequences
                                sequences = get_counts_from_seq(alignment.SEQ, int(config["DEFAULT"]["kmer"]))
                                edges = get_edges(sequences)

                                print("Generating plot")
                                
                                g1 = generate_plot(edges, alignment.NAME)
                               
                                lineCount += 1

                                # is_loop = loop_test(g1)
                                # if is_loop[0]:
                                #     print("\nLoop found")
                                #     loopCount += 1
                                #     save_graph(g1, is_loop[1], alignment, file)
                                #     #  todo 10 (general) +0: log here

                                    
                                # else:
                                #     print("\nNo loop found")
                                    
                                    
                            print("Loop rate: " + str(round(((loopCount/lineCount)*100), 2)) + "%\n")

def main():
    process_data()    
    #g1 = test_plot("ACTGAGTACCATGGAC",k=4)


if __name__ == "__main__":
    main()
