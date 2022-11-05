# Code Documentation for mygeneboleh's DSA4262 project

## Purpose of script 
The following document contains instructions to run the m6A classifier determined by mygeneboleh, as part of the final project for DSA4262 Sense-making Case Analysis : Health and Medicine for Academic Year 2022/23

## Installing Git
We will first need to install Git from [here](https://git-scm.com/download)
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/git_home.png)


## Installing VS Code
Code can be run with any editor of your choice, but this documentation will be using Visual Studio Code (VS Code).
This can be downloaded from [here](https://code.visualstudio.com/download) 
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/vs_download.png)

After selecting your operating system and opening the application, you will be on VS Code's homepage, which should look like this :
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/vs_home.png)

## Setting up VS Code
The first step would be to clone the GitHub repository onto your local machine.
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/vs_clone.png)


At the homepage  (displayed above), select the option 'Clone Git Repository...', upon which you will be asked to provide the repository URL :
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/vs_url.png)

Enter https://github.com/shienkoh/mygeneboleh.git, which can be retrieved from GitHub :
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/git_url.png)

Select the local directory you wish to clone the repository to, and you are all set!

## Running the script

Now, onto running the script itself.

The script has two inputs :
1) The path to the classifier
2) The path to the dataset

The former has been uploaded onto the GitHub repository itself, saved as `finalized_model.sav`

The latter has also been uploaded, named as `evaluator.json`

> Since the script, model and dataset are all within the same directory, the 2 paths are simply `finalized_model.sav` and `evaluator.json`

More precisely, the following command should be executed :

```python
%run script3.py -ipath 'finalized_model.sav' 'evaluator.json'
```

The steps above can all be found on the give template, `template.ipynb`

Hence all you need to do is run `template.ipynb` by opening the file on VS Code and then running the notebook :
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/run_all.png)

The script will output a csv filed titled `data_with_preds_and_scores.csv` onto the directory :

![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/output_example.png)

Alternatively, if you wish to view the dataframe directly on the editor, you can simply run the following commands :
```python
output = pd.read_csv('data_with_preds_and_scores.csv')
output
```
Again, this has been added to `template.ipynb` so the dataframe will appear once the notebook completes its run

