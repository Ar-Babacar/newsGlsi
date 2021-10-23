import requests

BASE = "http://127.0.0.1:5000/"

#data = [{"Titre": "Article1", "Categorie":"informations", "Contenu":"random texte you know"},
        #{"Titre": "Article2", "Categorie":"informations", "Contenu":"random texte you know1"},
    
        #{"Titre": "Article3", "Categorie":"Sport", "Contenu":"random texte you know3"}]

#for i in range(len(data)):
    # response = requests.put(BASE + "article/" + str(i), data[i])
    # print(response.json())



#input()

response = requests.patch(BASE + "article/1", {"Titre":"Babs mbengue","Categorie":"Sport"})
print(response.json()) 