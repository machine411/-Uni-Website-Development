// a1680043
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

class AVL
{
	struct node
	{
	    int mid;
	    node* left;
	    node* right;
	   // int height;
	};
	node* root;
public:
	AVL()
	{
		root = NULL;
	}

	int get_balance(node* n)
	{
		if (n == NULL) return 0;
		else return height(n->left) - height(n->right);
	}

	void In(int num)
	{
		root = Insert(root,num);
	}

	node* set_node(int num)
	{
		//cout << "SET: " <<num << endl;
		node* newnode = new node();
		newnode->mid = num;
		newnode->left = NULL;
		newnode->right = NULL;
		return newnode;
	}

	node* Insert(node* n, int data)
	{

		//cout <<"Insert: "<<data << endl;
		if (n == NULL)
			{
				n = set_node(data);   										// insert the root
			}
		else if (data > n->mid)
			{
				//cout << ">" << endl;
				n->right = Insert(n->right,data);
				if (height(n->right)-height(n->left) == 2)
				{
					//cout << " > de zhuan" << endl;
					if (data > n->right->mid) n = left_rotation(n);		//RR
					else n = RL_rotation(n);								//RL
				}

			}
		else if (data < n->mid)
			{	//cout << "<" <<endl;
				if (n->left == NULL)
				{
					//cout<< "Left is NULL" << endl;
				}
				n->left = Insert(n->left,data);
				//cout<< "ddd" << endl;
				if (height(n->left)-height(n->right) == 2)
				{
						//cout<<"jin "<< endl;
					if (data < n->left->mid)
						n = right_rotation(n);
					else
						n = LR_rotation(n);								//LR
				}
			}
		return n;
	}

	node* left_rotation(node* &root)
	{
		node* temp = root->right;
		root->right = temp->left;
		temp->left = root;
		return temp;
	}

	node* right_rotation(node* &root)
	{
		node* temp = root->left;
		root->left = temp->right;
		temp->right = root;
		return temp;
	}

	node* LR_rotation(node* &root)
	{
		root->left = left_rotation(root->left);
		return right_rotation(root);
	}

	node* RL_rotation(node* &root)
	{
		root->right = right_rotation(root->right);
		return left_rotation(root);
	}

	void Delete(int x)
	{
		root = Delete(root,x);
	}

	node* find_min(node* n)
	{
		//cout << "find_min" << endl;
		if (n == NULL) return NULL;
		else if (n->left == NULL) return n;
		else return find_min(n->left);
	}

	node* find_max(node* n)
	{
		//cout << "find_max" << endl;
		if (n == NULL) return NULL;
		else if (n->right == NULL) return n;
		else return find_max(n->right);
	}

	node* Delete(node* n, int x)
	{
		//cout << "Delete: " << x << endl;
		node* temp;
		if (n == NULL)
		{
			return n;
		}
		// Find the position
		else if (x < n->mid)
		{
			//cout << "Find position" << endl;
			n->left = Delete(n->left,x);					// Left side of root
		}

		else if (x > n->mid)
		{
			n->right = Delete(n->right,x);					// Rigth side of root
			//cout << 3323 << endl;
		}
		// One or zero child
		else if (n->left == NULL)
		{
			//cout << n->mid << endl;
			//cout << "NULL" << endl;
			if (n->right == NULL)
			{	//cout << "BOTH NULL" << endl;
				n = NULL;		// Both side NULL
				//cout << n->mid << endl;
			}
			else
			{
				n = n->right;
			}
			//cout <<"df"<< endl;
		}
		else if (n->right == NULL)
		{
			n = n->left;
		}
		// Two children
		else if (n->left != NULL && n->right != NULL)
		{
			//cout << "Two children" << endl;
			//cout << n->mid << endl;
			temp = find_max(n->left);
			n->mid = temp->mid;
			//cout << n->mid << endl;
			n->left = Delete(n->left,n->mid);
			//cout <<"jie wei "<< n->right->mid << endl;
		}
		/*
		if (n == NULL)
		{
			cout << "IS NULL" << endl;
		}
		else
		{
			cout <<"NOT NULL: " <<n-> mid << endl;
		}
*/
		if (n != NULL)
		{
			//cout << "balance R-L " <<height(n->left)-height(n->right)<< endl;

			//cout << 22212 << endl;
			if (height(n->right)-height(n->left) == 2)
			{	//cout << "R > L" << endl;
				if (height(n->right->left) <= height(n->right->right))
				{
					n = left_rotation(n);
				}
				else
				{
					n = RL_rotation(n);
				}
			}

			else if (height(n->left)-height(n->right) == 2)
			{	//cout << "L > R" << endl;
				if (height(n->left->left) >= height(n->left->right))
				{
					//cout <<" R " << endl;
					n = right_rotation(n);
				}
				else
				{
					//cout <<" LR " << endl;
					n = LR_rotation(n);
				}
			}

				//cout << 333 << endl;

		}

		return n;
	}


	int height(node* n)
	{
		//cout <<"n->mid"<< n->mid <<endl;
		if (n == NULL)
		{
		//	cout << "height" << endl;
			return 0;
		}
		else
		{//	cout <<"+1" << endl;
			return max(height(n->left),height(n->right)) + 1;
		}
	}

	void inorder()
	{
		inorder(root);
	}

	void inorder(node* n)
	{
		if (n == NULL) cout << "EMPTY" << endl;
		else
		{
			if (n->left != NULL) inorder(n->left);
			cout << n->mid << " ";
			if (n->right != NULL) inorder(n->right);
		}
	}

	void postorder()
	{
		postorder(root);
	}

	void postorder(node* n)
	{
		if (n == NULL) cout << "EMPTY" << endl;
		else
		{
			if (n->left != NULL) postorder(n->left);
			if (n->right != NULL) postorder(n->right);
			cout << n->mid <<" ";
		}
	}

	void preorder()
	{
		preorder(root);
	}
	void preorder(node* n)
	{
		if (n == NULL) cout << "EMPTY" << endl;
		else
		{
			cout << n->mid << " ";
			if (n->left != NULL) preorder(n->left);
			if (n->right != NULL) preorder(n->right);
		}
	}

	void print(string token)
	{
		if (token == "IN")
		{
			inorder();
       		cout << endl;
		}
		else if (token == "PRE")
		{
			preorder();
       		cout << endl;
		}
		else if (token == "POST")
		{
			postorder();
       		cout << endl;
		}
	}
};
/*
int sstream_counter(string in)
{
	stringstream kk(in);
	int num = 0;
	string t;
	while(kk >> t)
	{
		num++;
 	}
  	return num;
}
*/
int get_value(string token)
{
	token.erase(token.begin());
	std::string::size_type sz;
	int ans = stoi(token,&sz);
	return ans;
}

int main(int argc, char const *argv[])
{
	string input;
  input="D16 D13 A40 A61 A61 D1 A27 A60 A46 D11 D94 A86 D5 D72 D85 A20 D36 A20 A1 D80 A40 A15 A38 D75 A10 A5 D13 D38 PRE";
	//getline(cin,input);
	AVL* avl = new AVL();
	stringstream ss(input);
	string token;
	string output_operate;
	//int length = sstream_counter(input);
	//string array_of_token[length];
	//int a = 0;

	while (ss >> token)
	{
		switch (token[0])
		{
			case 'A':
			//cout << "CASE A: " << get_value(token)<< endl;
				avl->In(get_value(token));
				break;
			case 'D':
			//cout << "CASE D" << endl;
				avl->Delete(get_value(token));
				//cout << "finish D" << endl;
				break;
			case 'I':
				avl->print(token);
				break;
			case 'P':
				avl->print(token);
				break;
			case ' ':
				break;
		}
	}
}
