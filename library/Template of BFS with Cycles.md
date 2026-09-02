---
tags:
  - type/lit
  - topic/learning
  - status/archive
---

## Text

``` C++
void BFS(vector<vector<int>> & graph, int n, int start) {
	
	// init states
	// visited uses 1-based index!!!
	vector<int> visited(n+1, 0); 
	
	// queue for level
	queue<int> q; // queue<int> q(); are declaration for a function void -> queue
	
	// on event push, visited should be change.
	queue.push(start);
	visited[start] = 1;
	
	while (!q.empty()) {
		auto current_node = q.front();
		// Do Not Forget to POP!
		q.pop();
		
		for (neb: graph[current_node]) {
			if (!visited[neb]) {
				q.push(neb);
				visited[neb] = 1;
			}
		}
		
		
	}
	
}

```

---

## Thoughts