#include "args_parser.hpp"

ArgsParser::ArgsParser() : desc_("Allowed options") {
    namespace po = boost::program_options;
    // clang-format off
    desc_.add_options()
        ("help,h",                                                                      "produce help message")
        ("password,p",  po::value<decltype(password_)>(&password_)->required(),         "password to be encoded")
        ("salt,s",      po::value<decltype(salt_)>(&salt_),                             "salt")
        ("iter,i",      po::value<decltype(iter_)>(&iter_)->default_value(10),          "iterations number")
        ("saltsize,z",  po::value<decltype(saltSize_)>(&saltSize_)->default_value(64),  "generated salt size, bytes (ignored when -s is set)")
        ("keysize,k",   po::value<decltype(keySize_)>(&keySize_)->default_value(64),    "key size, bytes");
    // clang-format no
}

void ArgsParser::Parse(int argc, char* argv[]) {
    namespace po = boost::program_options;
    po::store(po::parse_command_line(argc, argv, desc_), vm_);
}

void ArgsParser::Validate() { boost::program_options::notify(vm_); }

const boost::program_options::options_description& ArgsParser::Description()
    const {
    return desc_;
}

bool ArgsParser::Help() const { return vm_.count("help"); }

const std::string& ArgsParser::Password() const { return password_; }

const std::string& ArgsParser::Salt() const { return salt_; }

std::size_t ArgsParser::Iter() const { return iter_; }

std::size_t ArgsParser::KeySize() const { return keySize_; }

std::size_t ArgsParser::SaltSize() const { return saltSize_; }
