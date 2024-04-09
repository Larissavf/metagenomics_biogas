# metagenomics_biogas
##### Larissa Voshol, Marian Hasan & Sven Schoonen | 31-03-2024 | Bio informatica 2 | versie 1

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

Maar voordat je hem wilt runnen moet je de volgende stappen hebben uitgevoerd.

__Opstarten conda env__  
`
Conda activate env.yaml 
`
__Install diamond__
Github repo:
Plaats het op de locatie waar ook de snakemake file staat.

__Run Snakemake__  
`
snakemake --snakefile Snakemake -c 2
`  

## Introduction  
Wat is het doel van deze repo  

__Het onderzoek__   

> De bacterieele community in deze reactor veranderd ook door de tijd, en dit heeft functionele gevolgen: soms valt de methaanproductie uit, of wordt de mix van, methaan en andere gassen verstoord. De vraag is dan of er iets te zien is aan de community op die momenten wat kan verklaren waarom de abiotische factoren veranderen.

Een bijpassende onderzoeksvraag zou als volgt kunnen zijn:

- ﻿﻿Wat is de samenstelling van de inhoud van de biogasreactor op 4 verschillende locaties, boven, midden, onder en het plaques?
- ﻿﻿Op welke manier kan deze samenstelling de methaanproductie beïnvloeden?

achtergrondinfo over de bacterien en waar we naar kijken.

__De pipeline__  
wat is de input  
workflow  

## Project structuur


## Help  
Voor verdere vragen kan je terecht bij de makers van deze repo.

Larissa Voshol: l.voshol@st.hanze.nl  
Marian Hasan: m.hasan@st.hanze.nl  
Sven Schoonen: s.schoonen@st.hanze.nl
