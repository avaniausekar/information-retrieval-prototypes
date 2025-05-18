import collections
class BSBIIndex(BSBIIndex):
    def invert_write(self, td_pairs, index):
        """Inverts td_pairs into postings_lists and writes them to the given index

        Parameters
        ----------
        td_pairs: List[Tuple[Int, Int]]
            List of termID-docID pairs
        index: InvertedIndexWriter
            Inverted index on disk corresponding to the block       
        """
        ### Begin your code
        td_dict = collections.defaultdict(list)
        for t,d in td_pairs:
            td_dict[t].append(d)
        td_dict2 = {k: v for k, v in sorted(td_dict.items(), key=lambda item: item[0])}
        for key,val in td_dict2.items():
            sorted_val = sorted(val)
            index.append(key,sorted_val)

        ### End your code
