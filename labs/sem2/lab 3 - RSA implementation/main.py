import getopt
import sys
import crypto
import json

'''
prints an error message and quits program with exit code 0

:param msg: the contents of the error message to print
'''
def error(msg:str):
    print("Error: " + str(msg))
    quit()

'''
gets command line arguments and executes playfair cipher
'''
def main(): 
    opts = None
    argv = sys.argv[1:] #first argument is file name ("main.py")
  
    #get the arguments
    try: 
        #"args" is just any unused parameters (i.e. with no flags)
        opts, args = getopt.getopt(argv, "c:p:i:o:hm:")
    except: 
        error("invalid parameters")
  
    mode = None
    output_file = None
    input_file = None
    lines = None
    cipher = None
    password = None

    #read through the parameteres
    for opt, arg in opts:
        if opt == "-c":
            cipher = arg
        elif opt == "-p":
            try:
                with open(arg, mode="r") as f:
                    password = json.loads("".join([line.removesuffix("\n") for line in f.readlines()]))
            except:
                password = None
        elif opt == "-i":
            input_file = arg
        elif opt == "-o":
            output_file = arg
        elif opt == "-h": #help mode
            print(
                str("=" * 50),
                "This program implements encryption, decryption, and key generation for multiple ciphers.",
                "",
                "Parameters:",
                "-c <cipher>\t cipher type (required)",
                "-m <mode>\t program mode (\"encrypt\" or \"decrypt\" or \"gen\") (required)",
                "-p <password>\t file containing JSON-encoded password to use (optional)",
                "-i <file>\t specify input file for cipher function (optional)",
                "-o <file>\t specify output file for cipher function (optional)",
                "-h\t\t get program usage instructions (optional)",
                "",
                "Supported Ciphers:",
                crypto.format_ciphers(),
                str("=" * 50),
                sep="\n",
                end="\n"
            )
            quit()
        elif opt == "-m":
            mode = arg

    #check for valid mode
    if not(mode == "gen" or mode == "encrypt" or mode == "decrypt"):
        error("invalid mode")
    
    #initialize the cipher
    c = crypto.get_cipher(cipher, password)
    final = None

    #check for valid cipher
    if cipher == None or c == None:
        error("invalid cipher")

    #get the input
    if input_file != None:
        try:
            lines = c.read_file(input_file, mode)
        except:
            error("invalid input file")
    elif not(mode == "gen"):
        lines = input("Enter input: ")

    
    #perform the cipher/key generation
    if mode == "gen":
        keys = json.dumps(c.encode_keys())
        #output the generated keys
        if output_file != None:
            try:
                f = open(output_file, "w")
                f.write(keys)
                f.close()
            except:
                error("invalid output file")
        else:
            print(keys)
        quit()
    elif mode == "encrypt":
        final = c.encrypt(lines)
    elif mode == "decrypt":
        final = c.decrypt(lines)
    else:
        error("invalid mode")

    #output the result
    if output_file != None:
        try:
            write_type = "wb" if type(final) is bytes else "w"
            f = open(output_file, write_type)
            f.write(final)
            f.close()
        except:
            error("invalid output file")
    else:
        print(final)

#run the program
main() 