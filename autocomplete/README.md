## An Autocomplete System

This functionality helps users to find and select from a pre-populated list of values as they type, reducing the amount of typing needed and making the input process faster and more efficient.

### Can be Implemented With
1. Trie
2. N-gram models
3. In memory Cache - Redis
4. Inverted Index
5. Using Predictive Machine Learning Models (harder to maintain)

### Points to Ponder
1. How to efficiently store the suggestions ? 
2. How to make search retrieval faster ?
3. How to handle typos ?
4. Should caching be client side or server side ?
5. Which type of Database or datastore to use for storage?

## References
- https://medium.com/pinterest-engineering/rebuilding-the-user-typeahead-9c5bf9723173
- https://systemdesignschool.io/
- http://oldblog.antirez.com/post/autocomplete-with-redis.html