class Solution {
    public int minCost(int n, int[][] edges) {

        List<List<int[]>> graph = new ArrayList<>();
        boolean[] visited = new boolean[n];
        int[] minCost = new int[n];
        Arrays.fill(minCost, (int)Math.pow(10,8));
        
        for(int i = 0; i < n; i++){
            graph.add(new ArrayList<>());
        }

        for(int[] edge : edges){
            int u    = edge[0];
            int v    = edge[1];
            int cost = edge[2];
            graph.get(u).add(new int[]{v, cost});
            graph.get(v).add(new int[]{u, 2 * cost}); // Add Switch Too
        }

        // Do Dijkstra's Algorithm
        minCost[0] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((n1, n2) -> Integer.compare(n1[1], n2[1]));
        pq.offer(new int[]{0, 0});
        while(!pq.isEmpty() && !visited[n-1]){
            int[] curr = pq.poll();
            if(visited[curr[0]]) continue;
            visited[curr[0]] = true;
            for(int[] nei : graph.get(curr[0])){
                if(visited[nei[0]]) continue;
                int newDis = nei[1] + minCost[curr[0]];
                if(minCost[nei[0]] > newDis){
                    minCost[nei[0]] = newDis;
                    pq.offer(new int[]{nei[0], newDis});
                }
            }
        }

        if(visited[n-1]) return minCost[n-1];
        return -1;
    }
}
