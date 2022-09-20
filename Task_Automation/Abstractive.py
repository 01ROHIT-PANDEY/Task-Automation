
import pickle
with open('AbstractModel_pkl' , 'rb') as f:
    lr = pickle.load(f)
def abstractive(text):
    output=lr.predict([text])
    str1 = ""
    # traverse in the string  
    for ele in output: 
        str1 += ele
    # return string  
    return str1 
        
   # print(output)
