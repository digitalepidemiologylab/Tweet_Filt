# Tweet_Filt - Author Axel Uran
This module will allow you to filter tweets in JSON format, based on a condition inputed as a string. In the future the idea is to implement new output formats for the function, ranging from a simple .txt file containing the selected tweets to a numpy array containing the vectorized version of the sentences to allow for direct applications in machine learning.

## Getting Started

To start working with this module you simply need to clone this project and add the data you want to filter in the Data folder. Right now the code only works with .gz files but other files could be easily implemented.
We added two simple templates to show what the different attributes of the run_all does, you can tinker with them to get a better grasp of the function.
The different attributes are rather self explanatory:
* path: will be the location where the Data is stored
* condition: will be the condition on which the filter will be based (see below for the nomenclature of this string)
* key: initialized for "text", changing this will allow for the filter to look at other information in the tweet object (e.g. "user", "coordinates"...)
* strip: initialized for True, this will allow the filter to remove the usernames, urls and hashtags from the analyzed field. By setting this attribute to false the analyzed fields will be left as is.

!Add a Dump folder to make the code run!

### Condition nomenclature

Will be a string that will be used by the filter to find the specific tweets. Will be case insensitive by default and the different condition will be implemented using this nomenclature:
* (): will group the tokens inside
* {}: case sensitive
* AND: and
* OR: or

Example text: My horse is not a dog!
* condition: ((cat OR dog) AND {horse}) will be ((False or True) and True) --> True

### Prerequisites

Most of the modules used in this project are native but if the machine does not find it, simply install it using pip (pip install <module that is missing>)

## Running the tests

TODO

## Deployment

TODO

## Built With

TODO
## Contributing

TODO

## Versioning

TODO

## Authors

* **Axel Uran** - *Initial work* - [Awowen](https://github.com/Awowen)

<!-- See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project. -->

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
