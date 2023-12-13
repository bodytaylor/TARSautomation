# TARSautomation

## Overview

The quest is to achieve 24 hours hotel onboarding with the help of pandas and openpyxl to transform data and inject the data with selenium in the DATA web. Currently version is beta 1.0.1, with 25 features, it is able to do 90% of onboarding process on the DATA web.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Automation Process](#automation-process)
  - [Data Processing](#data-processing)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)
- [Contact Information](#contact-information)
- [Acknowledgments](#acknowledgments)
- [Maintainer Information](#maintainer-information)

## Getting Started

This program designed for windows 10 operating system only.

### Prerequisites

 - python 3.8.1 x64 bit
 - pip 23.2.1
 - virtualenv
 - Microsoft Edge
 - Google Chrome

### Installation

1. Download source code from github or using git clone to local machine. 
2. Open CMD and install pip using command 
`code` python get-pip.py
3. Install virtualenv by run this command
`code` pip install virtualenv
4. Then run the "run this first.bat" for setup environment. Be patient it might take time.

## Usage

For onboarding process go to folder "hotel_workbook" and
create a new folder name as RID, inside the folder requires.
  1. Content creation book naming as "{hotel_rid} Content Book Hotel Creation.xlsm"
  2. Pricing book v1.7 naming as "{hotel_rid} Pricing Book Hotel Creation v1.7.xlsx"

### Automation Process

Start the program by double click on "tars_automation_run.bat" and it ready to Roll!

### Data Processing

Will update this section soonly!

## Configuration

On the first launch, the programe will ask for user credential of the DATAweb.
Then user can input Hotel RID that user wish to working on.
If user would like to switch the hotel, terminate the programe and start over.

## Troubleshooting

It is critical to ensure all the data in a Content Creation kit is correct.
With a current release, it able to handle Creation kit version 12 to 16.
For Content Creation kit version 17 and newer, it needs to edit sheet "Address&Setup" by delete row 29.

The main problem is login error and remote connection terminate, simply re-launch the program.

Main service not load properly?
re check the Content Creation kit, if descrition of the product not state as "Yes" the program will not read that line.

## Contributing

Considering send me the user feedback, your voice is matter!

## Changelog

28 November 2023 - release the first verion beta v1.0.1

## License

State the project's license and provide information about what others can and cannot do with the project.

## Contact Information

For request new features and report any issue contact: nantawat.sangkarn@accor.com

## Acknowledgments

Thank you for all creator of libraries listed on reqiurements.txt 

## Maintainer Information

developer: nantawat.sangkarn@accor.com 
