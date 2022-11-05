# Code Documentation for mygeneboleh's DSA4262 project

## Purpose of script 
The following documents contain instructions to run the m6A classifier determined by mygeneboleh, as part of the final project for DSA4262 Sense-making Case Analysis : Health and Medicine for Academic Year 2022/23

## Installing VS Code
Code can be run with any editor of your choice, but this documentation will be using Visual Studio Code (VS Code).
This can be downloaded from [here](https://code.visualstudio.com/download) 

After selecting your operating system and opening the application, you will be on VS Code's homepage, which should look like this :

## Setting up VS Code
The first step would be to clone the GitHub repository onto your local machine.

At the homepage  (displayed above), select the option 'Clone Git Repository...', upon which you will be asked to provide the repository URL :

This can be retrieved from GitHub :

Select the local directory you wish to clone the repository to, and you are all set!

## Running the script

Now, onto running the script itself.

The script has two inputs :
1) The path to the classifier
2) The path to the dataset

The former has been uploaded onto the GitHub repository itself, saved as `finalized_model.sav`

The latter has also been uploaded, named as `evaluator.json`

Since the script, model and dataset are all within the same directory, the 2 paths are simply `finalized_model.sav` and `evaluator.json`

More precisely, the following command should be executed :

```python
%run script3.py -ipath 'finalized_model.sav' 'evaluator.json'
```

The steps above can all be found on the give template, `template.ipynb`

Hence all you need to do is run `template.ipynb` by opening the file on VS Code and then running the notebook :


