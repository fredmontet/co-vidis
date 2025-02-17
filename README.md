Cō Vidis?
=========

**Cō Vidis?** [kʷoː ˈwɪːdɪs] ➡️ latin for "COVID-19, where are you going?"<br/>
A word game between COVID and Quō vādis (https://en.wikipedia.org/wiki/Quo_vadis)

A Dashboard to follow the state of the Coronavirus with a focus on Switzerland


Data Sources
------------

- **World** : https://github.com/CSSEGISandData/COVID-19
- **Switzerland** : https://github.com/daenuprobst/covid19-cases-switzerland


Get Started
-----------

Install the dependencies and start the notebook

    conda env create -f environment.yml
    conda activate co-vidis
    pip install -r requirements.txt
    jupyter notebook


How to Contribute
-----------------

Fork the repo and add the data

    git clone <your forked repository>
    cd <your forked repository>
    git clone https://github.com/CSSEGISandData/COVID-19 ./data/raw/COVID-19-master
    git clone https://github.com/daenuprobst/covid19-cases-switzerland ./data/raw/covid19-cases-switzerland-master


Author
------

Fred Montet (https://twitter.com/fredmontet)
