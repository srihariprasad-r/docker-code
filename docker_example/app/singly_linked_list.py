class Node:
    "Node is a class which takes data and pointer to next node instance as parameters and has head pointing to first node"
    def __init__(self, data):
        self.data = data
        self.next = None 
    
   
class linkedList:
    "Linkedlist"
    def __init__(self):
        self.head = None

    def print_list(self):
        cur_node = self.head
        while cur_node:
            print(cur_node.data)
            cur_node = cur_node.next        


    def find_next_node(self, data):
        find_node = self.head    
        while find_node:            
            if find_node.next.data == data:            
                return find_node.data , find_node.next
            else:
                find_node = find_node.next


    def length_list(self):
        cur_node = self.head
        total = 0
        while cur_node:
            cur_node = cur_node.next
            total += 1
        
        return total


    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node


    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return True
        
        last_node = self.head        
        while last_node.next:                                                 
            last_node = last_node.next             
        last_node.next = new_node            


    def insert_after_node(self, pre_node, data):
        _ , previous_node = self.find_next_node(pre_node)        
        inserted_node = Node(data)
        inserted_node.next = previous_node.next        
        previous_node.next = inserted_node
        return True
    """"
        if not pre_node:
            return False
        else:
            new_node = Node(data)
            new_node.next = pre_node.next
            pre_node.next = new_node
    """

    def delete_a_node(self, data):
        node_to_delete = Node(data)
        if node_to_delete is None:
            return False
        else:
            cur_node = self.head  
            prev_node = self.head                  
            while cur_node.next:
                if cur_node.data == data:                    
                    prev_node.next = cur_node.next
                    cur_node.next = None
                else:
                    prev_node = cur_node
                    cur_node = cur_node.next


    def reverse_linked_list(self):
        cur_node = self.head
        prev_node = None
        while cur_node:
            next_node = cur_node.next            
            cur_node.next = prev_node
            prev_node = cur_node
            cur_node = next_node            
        self.head = prev_node                


    def merge_two_list(self, list2):
        node1 = self.head
        node2 = list2.head
        index_node = None

        if node1 is None:
            return node2
        elif node2 is None:
            return node1

        if node1 and node2:
            if node1.data <= node2.data:
                index_node = node1
                node1 = index_node.next     #moved the node to point to next element from head
            else:
                index_node = node2    
                node2 = index_node.next
            
            new_head = index_node   #set head to newly added node

        while node1 and node2:
            if node1.data <= node2.data:
                index_node.next = node1
                index_node = node1
                node1 = index_node.next
            else:
                index_node.next = node2
                index_node = node2
                node2 = index_node.next   
        
        if node1 is None:
            index_node.next = node2
        elif node2 is None:
            index_node.next = node1 
        
        return new_head                            

    def node_swap(self,swap_element, to_element):        
        
        if swap_element == to_element:  #swap doesn't occur when both elements are same
            return
    
        prev_node1 = None
        cur_node1 = self.head            

        while cur_node1 and cur_node1.data != swap_element:
            prev_node1 = cur_node1
            cur_node1 = cur_node1.next

        prev_node2 = None
        cur_node2 = self.head            

        while cur_node2 and cur_node2.data != to_element:
            prev_node2 = cur_node2
            cur_node2 = cur_node2.next            
        
        if prev_node1:
            prev_node1.next = cur_node2
        else:
            self.head = cur_node2                               #when element being swapped is head
        if prev_node2:                     
            prev_node2.next = cur_node1
        else:
            self.head  = cur_node1
        
        cur_node1.next, cur_node2.next = cur_node2.next, cur_node1.next     #switch pointers for current node
    
    def rotate_node(self, pos):
        cur_node = self.head
        prev_node = None

        pointer1 = self.head
        pointer2 = self.head

        count = 0

        while pointer1 and count < pos:
            prev_node = pointer1
            pointer1 =  pointer1.next
            pointer2 = pointer2.next
            count += 1
        
        pointer1 = prev_node                # as we are in next node

        while pointer2:
            prev_node = pointer2
            pointer2 = pointer2.next
        
        pointer2 = prev_node

        pointer2.next = self.head
        self.head = pointer1.next
        pointer1.next = None
        
        #prev_node.next = None

    def tail_to_head(self):
        pointer1 = self.head
        pointer2 = self.head
        
        prev_node = None
        next_node = None
        
        while pointer1 and pointer2:
            next_node = prev_node                    
            prev_node = pointer1
            pointer1 = pointer1.next

        pointer1 = prev_node
        pointer2 = next_node

        pointer1.next = self.head        
        pointer2.next = None                # disonnecting last but one node from link

        self.head = pointer1                # moving the head to last node


sll1 = linkedList()        
sll2 = linkedList()

#add elements to first linked list object
sll1.append(1)
sll1.append(4)
sll1.append(5)
sll1.append(6)


#add elements to second linked list object
sll2.append(2)
sll2.append(3)
sll2.append(7)
sll2.append(8)

#sll1.length_list()                                 #find length of linked list
#sll1.merge_two_list(sll2)                           
#sll1.print_list()
#sll1.insert_after_node(3,8)                         #inserts node after node that is passed
#sll1.print_list()
#sll1.delete_a_node(5)                               #removes a node
#sll1.print_list()
#sll1.reverse_linked_list()                          #reverses linked list
#sll1.print_list()
#sll2.node_swap(7,3)                                 # node swap 
#sll2.print_list()
#print("before rotating the list")
#print("=======================")
#sll1.print_list()
#sll1.rotate_node(2)                                 # rotating list based on position of a element
#print("after rotating the list")
#print("=======================")
#sll1.print_list()
sll1.tail_to_head()                                 # move tail as head in linked list
sll1.print_list()
