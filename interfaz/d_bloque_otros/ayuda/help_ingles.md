## Help for RM Requirements Management Software

### Index
- [Uploading Documents to the Database](#uploading-documents-to-the-database)
- [Queries](#queries)
- [Other](#other)
- [Settings](#settings)
- [Help](#help)

---

### Uploading Documents to the Database
1. Using the **Select File** button (which opens the file explorer), choose the PDF file containing the requirements. It will appear in the viewer window. Then, start the process by pressing the **LOAD** button.

   1.1. **Chapter hierarchy recognition**: The patterns it recognizes are:
        - `1.`
        - `1`
        - `1-`
        - `1)`

   1.2. **Unrecognized patterns**:
        - 1. If unrecognized, the recommended option is **Modify**, which involves converting the PDF into an editable format using external software to incorporate one of the recognized patterns and manage the document.  
        - 2. The other available option is **Force**. In this mode, the entire document will be treated as a single chapter, and all requirements will be at the same hierarchical level.  

   1.3. **Recognized or forced patterns**: A window will appear for selecting the project to which you want to add the requirements.

2. Once the project is selected, confirm to proceed. The upload process will be completed, displaying the content and allowing editing (if you wish to correct or delete anything).
3. The system will analyze the potential scope of the subsystems and suggest those that might be affected. You can select some or all as appropriate.

At the end, the requirements/document will be stored and linked to the corresponding project and subsystems.

---

### Queries
1. You can search for **documents**, **projects**, **subsystems**, and **requirements** (text and tables/figures) by selecting the desired option.
2. To list all items, simply press the **Query** button.
3. To perform a specific search, use the filters for **Documents**, **Projects**, and **Subsystems**.
   - You can apply a single filter or combine them. For example, you can select the documents of a specific project and a single subsystem.  
   - The requirements displayed will always be from the latest version of the document, if there is more than one.  
   - You can delete a file directly from the query viewer; this option will cascade-delete the document's requirements.  
   - You can also delete requirement tables/images from the viewer.

---

### Other
1. **Projects**:  
   - You can add new projects to the database to assign them documents and requirements.  
   - The recommended criterion is to use the name of the city where the project will be developed.  
   - You can also delete projects.
2. **Subsystems**:  
   - You can add new subsystems to the database.  
   - For a subsystem to be recognized in the scope analysis of a document/requirement, its keywords must be included in the associated `TOKENES.csv` file.  
   - You can also delete subsystems.
3. **Assign**:  
   - This option allows you to create relationships between documents and subsystems after uploading the document.  
   - It is designed for cases where you need to associate a document with another subsystem afterward.  
   - You can also delete associations.

---

### Settings
1. You can choose the language in which you want to work with this application. This version supports **Spanish**, **English**, and **French**.

---

### Help
1. Explanation of each of the options available in this version of the software.

---
