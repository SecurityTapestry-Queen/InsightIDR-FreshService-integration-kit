from InsightFunctions import *

clients = ['Lab','LOM','HSSD','MHC','ICS','GosM']

if __name__ == '__main__':

    for c in clients:

        with open('config.json', 'r') as configfile:

            config = json.load(configfile)

            if config[c]['enabled'] is True:
                Investigations(c)