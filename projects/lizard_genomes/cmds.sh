for PEP in angptl2 klhl13 lpar4 mars2 slc31a1; do exonerate -m protein2genome -q /home/skliver@mcb.nsc.ru/projects/lizards/sex_chr/check_rovatsos2016/Z_pep/${PEP}.pep -n 100 --showalignment --showtargetgff -t ~/data/genomes/anolis_carolinensis/ncbi/AnoCar2.0/anolis_carolinensis.fasta > anolis_carolinensis.${PEP}.gff & exonerate -m protein2genome -q /home/skliver@mcb.nsc.ru/projects/lizards/sex_chr/check_rovatsos2016/Z_pep/${PEP}.pep -n 100 --showalignment --showtargetgff -t ~/data/genomes/lacerta_bilineata/ncbi/LacBil/lacerta_bilineata.fasta > lacerta.bilineata.${PEP}.gff & exonerate -m protein2genome -q /home/skliver@mcb.nsc.ru/projects/lizards/sex_chr/check_rovatsos2016/Z_pep/${PEP}.pep -n 100 --showalignment --showtargetgff -t ~/data/genomes/lacerta_viridis/ncbi/ASM90024590v1/lacerta_viridis.fasta > lacerta_viridis.${PEP}.gff & exonerate -m protein2genome -q /home/skliver@mcb.nsc.ru/projects/lizards/sex_chr/check_rovatsos2016/Z_pep/${PEP}.pep -n 100 --showalignment --showtargetgff -t ~/projects/lizards/Darevskia/darevskia_valentini/de_novo/assemblies/platanus_rnaseq/darevskia_valentini.dobby.v3.1000.fasta > darevskia_valentini.${PEP}.gff; done


for PEP in angptl2 klhl13 lpar4 mars2 slc31a1; do exonerate -m protein2genome -q /home/skliver@mcb.nsc.ru/projects/lizards/sex_chr/check_rovatsos2016/Z_pep/${PEP}.pep -n 100 --showalignment --showtargetgff -t ~/data/genomes/anolis_carolinensis/ncbi/AnoCar2.0/anolis_carolinensis.fasta > anolis_carolinensis.${PEP}.gff &  done
