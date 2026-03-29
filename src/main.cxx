#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/rand.h>

#include <boost/algorithm/hex.hpp>
#include <boost/json/src.hpp>
#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

#include "args_parser.hpp"

const char *g_help_string = "Usage: pbkdf2 [OPTIONS]\n"
                            "Derive key with PKCS5 PBKDF2 HMAC function and "
                            "automatically generated or given salt. "
                            "Makes use of SHA-512 function.\n"
                            "Output is given as JSON-string with hash and salt as hex-strings.\n";

int main(int argc, char *argv[]) {
    ArgsParser args;
    try {
        args.Parse(argc, argv);
        if (args.Help()) {
            std::cout << g_help_string << std::endl;
            std::cout << args.Description() << std::endl;
            return 0;
        }
        args.Validate();
    } catch (const boost::program_options::error &err) {
        std::cerr << "Error: " << err.what() << std::endl;
        std::cout << args.Description() << std::endl;
        return 1;
    }

    std::vector<unsigned char> salt;
    if (!args.Salt().empty()) {
        boost::algorithm::unhex(args.Salt(), std::back_inserter(salt));
    } else {
        salt.resize(args.SaltSize());
        if (RAND_bytes(salt.data(), static_cast<int>(salt.size())) != 1) {
            std::cerr << "Error: " << ERR_error_string(ERR_get_error(), NULL) << std::endl;
            return 1;
        }
    }
    std::vector<unsigned char> hash(args.KeySize());
    if (PKCS5_PBKDF2_HMAC(args.Password().c_str(), static_cast<int>(args.Password().size()),
                          salt.data(), salt.size(), args.Iter(), EVP_sha512(),
                          static_cast<int>(hash.size()), hash.data()) != 1) {
        std::cerr << "Error: " << ERR_error_string(ERR_get_error(), NULL) << std::endl;
        return 1;
    }

    boost::json::object jsonObject;
    std::ostringstream hexHash;
    boost::algorithm::hex_lower(hash, std::ostream_iterator<unsigned char>(hexHash, ""));
    jsonObject["hash"] = hexHash.str();
    if (args.Salt().empty()) {
        std::ostringstream hexSalt;
        boost::algorithm::hex_lower(salt, std::ostream_iterator<unsigned char>(hexSalt, ""));
        jsonObject["salt"] = hexSalt.str();
    }
    std::cout << boost::json::serialize(jsonObject) << std::endl;

    return 0;
}
