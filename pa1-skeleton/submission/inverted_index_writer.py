class InvertedIndexWriter(InvertedIndex):
    """"""
    def __enter__(self):
        self.index_file = open(self.index_file_path, 'wb+')              
        return self

    def append(self, term, postings_list):
        """Appends the term and postings_list to end of the index file.

        This function does three things, 
        1. Encodes the postings_list using self.postings_encoding
        2. Stores metadata in the form of self.terms and self.postings_dict
           Note that self.postings_dict maps termID to a 3 tuple of 
           (start_position_in_index_file, 
           number_of_postings_in_list, 
           length_in_bytes_of_postings_list)
        3. Appends the bytestream to the index file on disk

        Hint: You might find it helpful to read the Python I/O docs
        (https://docs.python.org/3/tutorial/inputoutput.html) for
        information about appending to the end of a file.

        Parameters
        ----------
        term:
            term or termID is the unique identifier for the term
        postings_list: List[Int]
            List of docIDs where the term appears
        """
        ### Begin your code
        encoded_postings = self.postings_encoding.encode(postings_list)
        start_position = self.index_file.seek(0, 2)
        length_postings_list = self.index_file.write(encoded_postings)
        self.terms.append(term)
        self.postings_dict[term] = (start_position,len(postings_list),length_postings_list)
        ### End your code
