Design Improvements
+ make the Gantt Chart container increase in height with the number of separate rows in the chart
+ make Gantt Chart scrollable in height and width directions
+ app bar buttons are transparent
+ dollar values should be displayed with comma separators

Model Structure Improvements
+ new top-level model for Projects. Should have:
    + a name
    + a start date
    + a project entails a collection of multiple equipment sales (each equipment sale having the payment milestone attached as per current structure)
+ amend EquipmentSale model to allow selection of Vendor or Customer sale (default is Vendor)

I/O Improvements
+ Gantt Chart should support both projects that contain multiple equipment sales and single equipment sales
+ where there are multiple equipment sales, the rows in the gantt shart should be grouped by the different equipment sales
+ allow CRUD operations to all objects directly in the Gantt Chart module

