from tqdm import tqdm

DEFAULT_SEARCH_LIMIT=25

class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = dict()
    def __str__(self):
         return json.dumps({"label":self.label,"data":self.data})
    
    def addChild(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]
    
    

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word):
        current_node = self.head
        word_completed = True
        
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_completed = False
                break
        
        # For ever new letter, create a new child node
        if not word_completed:
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                i += 1
        
        # store the full data at the end node so we don't need to
        # travel back up the tree to reconstruct the word
        current_node.data = word
    
    def has_word(self, word):
        self.check_if_input_empty(word)

        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        
        # check if end node have data
        if exists:
            if current_node.data == None:
                exists = False
        
        return exists
    
    @staticmethod
    def check_if_input_empty(prefix):
        if prefix == None or prefix=="":
            raise ValueError('Requires not none and non empty value')
            return
        
    
    def start_with_prefix(self, prefix,limit=DEFAULT_SEARCH_LIMIT):
        """ Returns a list of all words in tree that start with prefix """
        self.check_if_input_empty(prefix)
        words = list()
        limit=limit-1
        # get_the_end
        top_node = self.head
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else:
                # Prefix not in tree, go no further
                return words
        
        # Get words under prefix
        if top_node == self.head:
            queue = [node for key, node in top_node.children.items()]
        else:
            queue = [top_node]
        
        # do bfs
        limit_count=0
        while queue:
            if(limit_count>limit):
                break
            current_node = queue.pop()
            if current_node.data != None:
                limit_count=limit_count+1
                words.append(current_node.data)
            queue = [node for key,node in current_node.children.items()] + queue
        
        return words
    
    def getData(self, word):
        """ This returns the data of the node identified by the given word """
        if not self.has_word(word):
            raise ValueError('{} not found in trie'.format(word))
        
        # Race to the bottom, get data
        current_node = self.head
        for letter in word:
            current_node = current_node[letter]
        
        return current_node.data
    def bulkUpdate(self, word_list):
        """ Bulk update Trie """
        total_words=len(word_list)
        if total_words==0:
            raise ValueError('cant update empty list')
            
        pbar=tqdm(total = total_words)
        for word in word_list:
            pbar.update(1)
            self.add(word)
        return "sucess"

