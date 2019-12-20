# Challenges of working with IATI Data

IATI was designed for flexibility.
Within the aid sector multiple different organizations and governments work towards dramatically different goals, with different approaches and different ways of working.
This diversity in the sector is reflected in the IATI data.
For example; one organizations idea of an activity is not the same as another organizations.
Multiple currencies are used, but the particular currency (eg £, $ or €) is not always specified.
Different organizations update their projects at different times.
None of these examples are exactly a fault in the data, but rather reflect the complexity of the sector and the multiple languages, cultures, backgrounds and motivations of the organizations involved in aid.
This needs to be borne in mind when analysing the data.
As a simple example; using the “language” tag to remove non-English entries does not remove all non-English entries.
This means that depending on the stopwords list used words like “pour” will cause French language entries to cluster, as “pour” is “for” in French, but also a valid word in English.
The point of this example is that the data will always require particularly careful examination of any filter or analysis, and even simple transformations do not always result in the expected outcome.
