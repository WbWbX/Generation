# Generation

## Download repository

```bash
git clone https://github.com/WbWbX/Generation.git
```

## Generate gridpacks
Download CMS generator package ([genproductions](https://github.com/cms-sw/genproductions)), and run `gridpack_generation.sh` script with the desired set of cards.
```bash
git clone -b mg27x https://github.com/cms-sw/genproductions.git
cd genproductions/bin/MadGraph5_aMCatNLO/
cp -r PATHTOGENERATION/CARDFOLDER cards/
./gridpack_generation.sh CARDFOLDER cards/CARDFOLDER
```
Further instructions on how to create cards for Madgraph can be found [here](https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO#Create_the_gridpacks_for_each_pr).

Useful  tutorial on MG options can be found [here](https://cp3.irmp.ucl.ac.be/projects/madgraph/attachment/wiki/MC4BSM2015/MC4BSM15_Tuto1_solution.pdf)
