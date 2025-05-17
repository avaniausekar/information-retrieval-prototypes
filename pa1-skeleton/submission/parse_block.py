class BSBIIndex(BSBIIndex):            
    def parse_block(self, block_dir_relative):
        """Parses a tokenized text file into termID-docID pairs

        Parameters
        ----------
        block_dir_relative : str
            Relative Path to the directory that contains the files for the block

        Returns
        -------
        List[Tuple[Int, Int]]
            Returns all the td_pairs extracted from the block

        Should use self.term_id_map and self.doc_id_map to get termIDs and docIDs.
        These persist across calls to parse_block
        """
        ### Begin your code
        term_doc_pairs = []
        file_dirs = sorted(os.listdir(os.path.join(self.data_dir, block_dir_relative)))
        for  direct in file_dirs:
            with open(os.path.join(self.data_dir, block_dir_relative, direct), 'r') as f:
                tokens = f.read().strip().split()
                doc_id = self.doc_id_map[os.path.join(block_dir_relative, direct)]
                for token in tokens:
                    term_id = self.term_id_map[token]
                    term_doc_pairs.append([term_id, doc_id])
        return term_doc_pairs

        ### End your code
