# metagenomics_biogas
##### Larissa Voshol, Marian Hassan & Sven Schoonen | 31-03-2024 | Bio informatica 2 | versie 1

## Purpose  
Dit is een pipeline voor een Metagenomics onderzoek. Er wordt hier gekeken naar minION reads, deze worden gerecalibreert vervolgens wordt er met kraken2 en biobakery gekeken naar de inhoud van de samples.

## Getting started

### Prerequisities  
Je moet anaconda or miniconda version 24.1.2 geinstalleerd hebben.

### Installing  
__Clone repo__  
`
git clone https://github.com/Larissavf/metagenomics_biogas
`  
__Start env__  
`
conda env create --file environment.yml
`  
### Usage   
De pipeline is samengesteld in snakemake, je moet het dus via snakemake runnen.  
__Run Snakemake__  
`
snakemake --snakefile Snakemake -c 2
`  

## Introduction  
Deze repo is gemaakt voor een metagenomics onderzoek van de inhoud van een Tricklebed reactor (TBR), die op het lab staat in de hanze. Dit is dan ook in uitvoering gedaan van de groep onderzoekers van dit project. Bij dit project:  
  
Is er dus een methode om biogas te produceren onderzocht, Dit wordt gedaan door het omzetten van biomassa in methaan met behulp van microben die zich bevinden in het rumen van koeien. Het rumen is het grootste gedeelte van de maag van een koe.    
  
Bij dit proces wordt vloeistof uit het rumen geëxtraheerd en samen met gras in een artificiële rumen reactor (ARR) gebracht. De microben die in de vloeistof afkomstig uit het rumen aanwezig zijn, produceren vervolgens vluchtige vetzuren (VFA's) middels fermentatie, een vorm van anaerobe respiratie. Anaerobe respiratie is een proces waarbij energie wordt geproduceerd in afwezigheid van zuurstof. Bij de fermentatie worden koolhydraten gedegradeerd tot VFA’s. ​Deze VFA's worden geëxtraheerd uit de ARR en in een biogasreactor geplaatst waar de methaan productie door de aanwezige microben plaatsvindt​.    
  
De productie van methaan wordt ook wel methanogenese genoemd. Deze microben gebruiken hiervoor waterstof en koolstofdioxide als substraten. De methanogenese reactie is een redoxreactie. Hierbij fungeert waterstof als de elektron donor en wordt deze geoxideerd. Koolstofdioxide wordt tijdens de reactie gereduceerd .   
  
Het geproduceerde methaan wordt vervolgens gezuiverd in een Tricklebed reactor (TBR). Naast de zuivering vindt er verdere methanogenese plaats. De methanogenese lijkt echter op sommige momenten te dalen​. Om de reden voor deze daling te achterhalen is er een metagenomics analyse uitgevoerd. Met metagenomics kan het genetisch materiaal van meerdere microben in een keer direct geanalyseerd worden. Hierdoor kan de focus gelegd worden op de functies, compositie en diversiteit van een gemeenschap aan microben, in plaats van het analyseren van individuele microben. Verder wordt metagenomics veel gebruikt omdat het de mogelijkheid bied om microben die moeilijk of niet te kweken zijn toch te bestuderen​.    

__Het onderzoek__   

> De bacterieele community in deze reactor veranderd ook door de tijd, en dit heeft functionele gevolgen: soms valt de methaanproductie uit, of wordt de mix van, methaan en andere gassen verstoord. De vraag is dan of er iets te zien is aan de community op die momenten wat kan verklaren waarom de abiotische factoren veranderen.

Een bijpassende onderzoeksvraag zou als volgt kunnen zijn:

- ﻿﻿Wat is de samenstelling van de inhoud van de biogasreactor op 4 verschillende locaties, boven, midden, onder en het plaques?
- ﻿﻿Op welke manier kan deze samenstelling de methaanproductie beïnvloeden?

We kijken dus naar de bacterien die aan methagonese doen.

__De pipeline__  

__input:__ .fastq files.
__output:__ kraken output files  
    kraken_report.log:  
        5 kolommen:  
            1. Percentage van de reads in een clade/taxon.  
            2. Aantal reads in clade  
            3. Aantal reads in clade maar niet verder classified  
            4. Code dat rank aangeeft, (U)nclassified, (D)omain, (K)ingdom, (P)hylum, (C)lass, (O)rder, (F)amily, (G)enus, (S)pecies  
            5. NCBI taxonomi ID  
            6. Taxonomic name  
    kraken_output.txt:  
        3 kolemmen:  
            1. Sequence ID  
            2. NCBI taxon ID  
            3. Samenvatting van taxon Ids die zijn gematched aan elke k-mer.  
  
In deze workflow hebben we gebruik gemaakt van de volgende tools:  
- NanoQC  
- NanoFilt  
- kraken  
- humann3?  
- dorado*  

* Dorado heeft zijn eigen snakmake bestand. Want deze is gebruikt voor het rebasecallen van de data. De input hiervan is fast5. 

## Project structuur
__Logboek__:  
Bevat het logboek, hierin kan je het proces zien van dit project.  

__Workflow__:  
Bevat de Snakefile, rules, config file en andere scripts gebruik voor dit project.  

## Help  
Voor verdere vragen kan je terecht bij de makers van deze repo.

Larissa Voshol: l.voshol@st.hanze.nl  
Marian Hasan: m.hasan@st.hanze.nl
Sven Schoonen: s.schoonen@st.hanze.nl
