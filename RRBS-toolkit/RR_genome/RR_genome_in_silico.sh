#!/bin/sh
#$ -l mem=10G
#$ -l h_vmem=20G

# usage :
# ../Scripts/BioInformatics/RR_genome_in_silico.sh <path to genome file> <recognition_sequence> <min_fragment_size> <max_fragment_size> <if_chromosomes_scaffolds_must_be_treated>

RR_GENOME_HOME=`dirname $0`
.  $RR_GENOME_HOME/../config.sh


##########
# Test if genome file is present

file=$1

if [ "$1" == "" ]; 
then
    echo "genome file is missing"
    echo "Usage : ./RR_genome_in_silico.sh <genome_file>"
    exit 1
fi


if [ ! -f "$file" ]
then
	echo "File '$file' do not exist"
	exit 1
fi



##########
# Test if fasta file suffix is .gz
# then gunzip

found=$(echo $file | grep -E '.gz(ip)?$')

if [ "$found" ]; 
then
    echo "gz extension"
    gunzip $file
fi


##########
# names of paths, file with or without suffix

# check if suffix is .fasta or .fa
found=$(echo $file | grep '.fasta$')
found2=$(echo $file | grep '.fa$')

if [ "$found" ] || [ "$found2" ]; 
then
    if [ "$found" ];
    then
	 # path to the file with file name without suffix
         file_without_suffix=${file%%.fasta}

	 # file name without suffix
	 file_without_suffix_basename=`basename "$file_without_suffix"`

    elif [ "$found2" ];
    then
         file_without_suffix=${file%%.fa}

	 file_without_suffix_basename=`basename "$file_without_suffix"`

    else 
         echo "file suffix unknown."
    fi
fi

# file name with suffix but without path
file_in=`basename "$file"`

# path without file name
path_in=`dirname "$file"`



##########
# other arguments

#argument #2 = recognition sequence (ie : CCGG for Msp1)
recognition_sequence=$2
#argument #3 = min fragment size, argument #4 = max fragment size (if min = 0 and max = -1, no size selection)
min_fragment_size=$3
max_fragment_size=$4
#argument #5 = enter "1" if chromosomes scaffolds must be treated
if_chromosomes_scaffolds_must_be_treated=$5



# Fasta file processing....

(


######### in silico DNA digestion
$PYTHON_EXECUTE $RR_GENOME_HOME/RR_genome_digestion.py $file $recognition_sequence $min_fragment_size $max_fragment_size $if_chromosomes_scaffolds_must_be_treated

if [ $? -ne 0 ]
then
    echo "fasta RR dig failed !!!"
    exit 1
else
    echo "fasta RR dig ok"
fi


if [ "$max_fragment_size" == "-1" ]; 
then
	new2=$file_without_suffix"_frag_in_silico_"$recognition_sequence".fasta"
else
	new2=$file_without_suffix"_frag_in_silico_"$recognition_sequence"_"$min_fragment_size"_"$max_fragment_size".fasta"
fi

#output_file_from_dig_genome=$file_without_suffix"_frag_in_silico_"$recognition_sequence"_"$min_fragment_size"_"$max_fragment_size".fasta"

##### in silico RR genome parameters
$PYTHON_EXECUTE $RR_GENOME_HOME/RR_genome_parameters.py $new2 $recognition_sequence

if [ $? -ne 0 ]
then
    echo "RR parameters failed !!!"
    exit 1
else
    echo "RR parameters ok"
fi


) 1> $path_in/RR_genome_in_silico.log 2>&1
