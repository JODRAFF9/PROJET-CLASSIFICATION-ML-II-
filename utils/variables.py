def nom_variable(nom, mode='vers_descriptif'):
    correspondance = {
        'CreditScore': "le score de crédit",
        'Geography': 'le pays de résidence',
        'Gender': 'le genre du client',
        'Age': "l'âge du client",
        'Tenure': 'la durée de relation client',
        'Balance': 'le solde du compte',
        'NumOfProducts': 'le nombre de produits souscrits',
        'HasCrCard': "la possession d'une carte crédit",
        'IsActiveMember': "le statut de membre actif",
        'EstimatedSalary': "le revenu annuel estimé",
        'Exited': "l'indicateur d'attrition"
    }
    inverse = {v: k for k, v in correspondance.items()}
    return correspondance.get(nom, nom) if mode == 'vers_descriptif' else inverse.get(nom, nom)
