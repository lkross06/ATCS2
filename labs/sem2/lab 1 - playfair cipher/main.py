import getopt
import sys
from playfair import PlayFair

'''
gets command line arguments and executes playfair cipher
'''
def main(): 
    opts = None
    argv = sys.argv[1:] #first argument is file name ("main.py")
  
    #get the arguments
    try: 
        #"args" is just any unused parameters (i.e. with no flags)
        opts, args = getopt.getopt(argv, "i:o:hm:")
    except: 
        print("Error: bad parameters") 
        quit()
  
    mode = None
    output_file = None
    readinput = False
    lines = None

    #read through the parameteres
    for opt, arg in opts:
        if opt == "-i":
            readinput = True
        elif opt == "-o":
            output_file = arg
        elif opt == "-h": #help mode
            print(
                "This program implements an encryption and decryption for the playfair cipher.",
                "",
                "Parameters:",
                "-m <mode>\t program mode (\"encrypt\" or \"decrypt\") (required)",
                "-i <file>\t specify input file (.txt) to encrypt (optional)",
                "-o <file>\t specify output file (.dat) for ciphertext (optional)",
                "-h\t\t get program usage instructions (optional)",
                "",
                sep="\n",
                end="\n"
            )
            quit()
        elif opt == "-m":
            mode = arg

    #get the input text based on specified parameters
    if readinput:
        try:
            f = open(arg, "r")
            lines = "".join([line.removesuffix("\n") for line in f.readlines()])
        except:
            print("Error: input not found")
            quit()
    else:
        lines = input("Enter input: ")
    
    #make a ciphering object
    pf = PlayFair("dragonsden") #TODO: get password from user????
    final = ""
    
    #perform the cipher based on mode parameter
    if mode == None:
        print("Error: no mode specified")
        quit()
    elif mode == "encrypt":
        final = pf.encrypt(lines)
    elif mode == "decrypt":
        final = pf.decrypt(lines.encode())

    #output the result
    if output_file != None:
        f = open(output_file, "wb")
        f.write(final)
        f.close()
    else:
        print("", final)

#run the stuff
main() 