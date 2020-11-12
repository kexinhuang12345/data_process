# tdc data_process



## [MOSES](https://github.com/molecularsets/moses) 


```bash

wget https://media.githubusercontent.com/media/molecularsets/moses/master/data/dataset_v1.csv 

mv dataset_v1.csv raw_data/moses.csv

python data_process/moses.py 

```


## [Paired data]

```bash

wget https://raw.githubusercontent.com/wengong-jin/iclr19-graph2graph/master/data/drd2/train_pairs.txt

wget https://raw.githubusercontent.com/wengong-jin/iclr19-graph2graph/master/data/qed/train_pairs.txt

wget https://raw.githubusercontent.com/wengong-jin/iclr19-graph2graph/master/data/logp04/train_pairs.txt

```

## [ZINC](https://github.com/microsoft/constrained-graph-variational-autoencoder/blob/master/data/get_zinc.py)

pls see https://github.com/microsoft/constrained-graph-variational-autoencoder/blob/master/data/get_zinc.py 

```bash

wget https://raw.githubusercontent.com/aspuru-guzik-group/chemical_vae/master/models/zinc_properties/250k_rndm_zinc_drugs_clean_3.csv 



```

