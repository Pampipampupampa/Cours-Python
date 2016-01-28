# EnergyPlusToFMU #

Mise à jour: 20160122

## Script Python ##
Les scripts ont été fortement modifiés pour améliorer:

 - La lisibilité du code
 - Le rendre compatible python2 et python3
 - Le docummenter
 - Le faire fonctionner correctement



## Script Bash ##
Les différents scripts nécessite un lien vers le compilateur et le linkeur.
Sur ce PC la configuration a été écrite comme ci-suit:

    ::--- Set up command environment.
    ::
    ::   Run batch file {vcvarsall.bat} if necessary.
    ::   Work through a hierarchy of possible directory locations.
    ::
    IF "%DevEnvDir%"=="" (
      :: 64 bit
      CALL "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\amd64\vcvars64.bat"  >nul 2>&1
      :: 32 bit
      ::CALL "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC2\vcvarsall.bat"  >nul 2>&1
      IF ERRORLEVEL 1 (
        ECHO Problem configuring the Visual Studio tools for command-line use
        GOTO done
        )
      )



## Utilisation ##
La commande ci-dessous permet de créer un fmu pour le fichier `<path_to_idf_file>`.
Il est nécessaire d’être dans le même dossier que le script `EnergyPlusToFMU.py`
L’argument `-d` est normalement là pour le debug mais sans celui-ci les fichiers
intermédiaires ne peuvent pas être supprimés.

    C:\Users\bois\Anaconda\envs\py34\python.exe .\EnergyPlusToFMU.py -d -i C:\EnergyPlusV8-4-0\Energy+.idd <path_to_idf_file>

Il est possible de lier un fichier météo en ajoutant ce fichier comme source:

    -w <path_to_weather_file>

Enfin l’option `-L` permet de conserver les fichiers intermédiaires.

Ainsi on transforme un fichier energy plus `.idf` en FMU `.fmu` en utilisant la commande suivante:

    C:\Users\bois\Anaconda\envs\py34\python.exe .\EnergyPlusToFMU.py -d -w <path_to_weather_file> -i C:\EnergyPlusV8-4-0\Energy+.idd <path_to_idf_file>

**Exemple:**

    C:\Users\bois\Anaconda\envs\py34\python.exe .\EnergyPlusToFMU.py -d -w "D:\Github\solarsystem\Meteo\Bordeaux\FRA_Bordeaux.075100_IWEC.epw" -i C:\EnergyPlusV8-4-0\Energy+.idd "D:\Github\Cours-Python\Work\Tools\EnergyPlusToFMU\Examples\Schedule\_fmu-export-schedule.idf"


## Utilisation du FMU: ##

 - Ajouter au PATH le dossier EnergyPlus
 - Simulations doivent finir à minuit et le début/fin de simulation doivent être définies en secondes
 - Une seule instance de RunPeriod est autorisée
 - Le pas de temps de EnergyPlus doit être le même que le pas de temps de synchronisation
 - Pendant les `Warm up period` et `autosizing` energy Plus ne fait aucuns échanges avec le programme maître
 - Résultats crées dans le dossier de travail actuel (ou la commande a été lancée) et est de la forme `Output_EPExport<instance_model_name>`



