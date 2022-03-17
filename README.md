# AAD-Repo

This repository contains the program we made for Advanced Analysis and Design. It is a restaurants' fridge database management system, with the database hosted on Azure and two applications available - desktop and web. 

Desktop Application
- This is for the chefs and head chefs.
- It allows for the removal of items from the fridge (all permissions), the generation of health reports (head chef only) and the management of staff (head chef only).
- The user can also signup for an account as a chef or head chef.

Web Application
- This is for the delivery drivers.
- It allows for the addition of items to a fridge database.
- The user can also signup for an account as a delivery driver.
- Drivers must have the correct door code and file type to upload items to the database.

Currently, both of these are local applications but in the future, it would be developed so that the web application, which is used by delivery drivers, is hosted online. This would likely be on an Azure cloud service. Additionally, the desktop application would be converted into a package, to remove the need for individual users to download the required Python libraries.
