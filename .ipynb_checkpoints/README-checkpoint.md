
### Question 1 (10 points)  
**Explain how the automated maze explorer works.**  
Your answer should include:
1. The algorithm used by the explorer  
2. How it handles getting stuck in loops  
3. The backtracking strategy it employs  
4. The statistics it provides at the end of exploration

**To answer this question:**
- Run the explorer both with and without visualization  
- Observe its behavior in different maze types  
- Analyze the statistics it provides  
- Read the source code in `explorer.py` to understand the implementation details  

**Your answer should demonstrate a clear understanding of:**
- The right-hand rule algorithm  
- The loop detection mechanism  
- The backtracking strategy  
- The performance metrics collected  

---

#### 1. Algorithm Used by the Explorer  
The maze explorer utilizes the **Right-Hand Rule** (a wall-following algorithm). It works by:
- Turning right whenever possible  
- If no right turn, move forward  
- If forward is blocked, turn left or backtrack  
- This algorithm guarantees reaching the exit in simply connected mazes.

---

#### 2. Handling Loops  
Right-hand rule may get trapped in loops if revisited cells aren't handled. The explorer handles this by:
- Tracking previously visited cells  
- Avoiding revisiting these cells  
- Effectively preventing endless circling in loops

---

#### 3. Backtracking Strategy  
Backtracking occurs when:
- The explorer reaches a dead end  
- It returns to a decision point with unexplored paths  
- Helps in continuing exploration efficiently  
- Backtracking is triggered by loop detection or dead ends

---

#### 4. Statistics at the End of Exploration  
The explorer prints:
- Total time taken  
- Total moves made  
- Number of backtrack operations  
- Average moves per second  

---

### Question 2 (30 points)  
**Modify the main program to run multiple maze explorers simultaneously.**  

Your solution should:
1. Run multiple explorers in parallel  
2. Collect and compare statistics from all explorers  
3. Display a summary of which explorer performed best  

**Hints:**
- Use `multiprocessing` (20 pts)  
- Use `MPI4Py` on multiple machines (30 pts)  
- Bonus: Use Celery + RabbitMQ  
- Do not visualize during parallel runs  
- Store results for comparison  

**Steps to Answer:**
- Study current explorer  
- Design parallel execution  
- Implement task distribution  
- Create comparison summary  

---

### Question 3 (10 points)  
**Analyze and compare performance of different explorers on the static maze.**

1. Run at least 4 explorers  
2. Compare metrics:
   - Total time taken  
   - Number of moves  
   - *Optional:* Backtracks  
3. Analyze and explain differences in performance  

---

### Question 4 (20 points)  
**Propose and implement enhancements to overcome limitations.**

Your answer should include:
1. Identified limitations  
2. Proposed improvements  
3. Modified code with documentation  

---

####  Analysis of Current Limitations

| Limitation | Description |
|------------|-------------|
| Inefficient Exploration | Right-hand rule can take long paths in large mazes |
| Repetitive Backtracking | Same paths retraced multiple times |
| Weak Loop Detection | Only last 3 moves tracked; not robust |
| No Path Optimization | Doesn’t guarantee shortest path |

---

####  Proposed Improvements

| Improvement | Description |
|-------------|-------------|
| A* Algorithm | Uses heuristics, finds shortest path efficiently |
| Visited Set | Prevents revisiting nodes, avoids loops |
| Enhanced Loop Detection | Tracks full path history |
| Optional: BFS | Guarantees shortest path without heuristics |

---

### Question 5 (20 points)  
**Compare enhanced explorer performance with original.**  

Run both on the static maze. Collect:

| Metric | Original | Enhanced (Avg.) |
|--------|----------|------------------|
| Total Time | 0.00 s | ~0.0025 s |
| Moves Made | 1279 | 127 |
| Backtracks | 0 | 0 |
| Moves/sec | 847,207 | ~64,078 |

---

####  Moves per Second (Enhanced Runs)

| Run | Time (s) | Moves | Moves/sec |
|-----|----------|-------|-----------|
| 1 | 0.00 | 127 | 93,353.77 |
| 2 | 0.00 | 127 | 90,345.42 |
| 3 | 0.01 | 127 | 13,820.68 |
| 4 | 0.00 | 127 | 60,793.95 |
| **Avg** | ~0.0025 | 127 | ~64,078 |

---

####  Key Improvements

- **Over 90% reduction** in move count  
- **Consistent performance** across runs  
- **Zero backtracking**, indicating optimal pathing  

---

####  Trade-offs

| Trade-Off | Description |
|-----------|-------------|
| Lower Moves/sec | Fewer steps make speed metric seem slower |
| Less Visual Debug Info | Fewer steps, less insight into logic |
| Generalization Risk | Enhanced pathing may depend on maze type |
| Timing Precision Limit | All results show 0.00s due to timer granularity |

---

###  Summary

| Explorer | Moves | Time (s) | Moves/sec | Efficient? |
|----------|-------|----------|------------|-------------|
| Original | 1279 | 0.00 | 847,207 |  No |
| Enhanced | 127 | ~0.0025 | ~64,078 |  Yes |

**Conclusion**:  
The enhanced explorer shows massive gains in efficiency and path optimality. Although moves/sec appears lower, it’s due to the reduced steps needed to reach the goal. Algorithms like **A*** and **BFS** are likely in use, delivering significantly better results in a more structured and optimized way.

