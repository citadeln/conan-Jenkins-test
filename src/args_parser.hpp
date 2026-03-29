#pragma once

#include <boost/program_options.hpp>
#include <cstddef>
#include <string>

class ArgsParser {
public:
    ArgsParser();
    void Parse(int argc, char *argv[]);
    void Validate();
    const boost::program_options::options_description &Description() const;
    bool Help() const;
    const std::string &Password() const;
    const std::string &Salt() const;
    std::size_t Iter() const;
    std::size_t KeySize() const;
    std::size_t SaltSize() const;

private:
    boost::program_options::variables_map vm_;
    boost::program_options::options_description desc_;
    std::string password_;
    std::string salt_;
    std::size_t iter_;
    std::size_t keySize_;
    std::size_t saltSize_;
};
