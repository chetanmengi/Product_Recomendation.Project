
import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './styles.css';

function App(){
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [summary, setSummary] = useState(null);\n  const [genLoading, setGenLoading] = useState(false);

  useEffect(()=>{
    fetchSummary();
  },[]);

  async function fetchSummary(){
    try{
      const res = await axios.get('http://localhost:8000/api/analytics/summary');
      setSummary(res.data);
    }catch(err){
      console.error(err);
    }
  }

  async function handleSearch(e){
    e.preventDefault();
    try{
      const res = await axios.post('http://localhost:8000/api/query', {query: query, k:5});
      setResults(res.data.results);\n      // fetch generated descriptions
      try{\n        setGenLoading(true);\n        const g = await axios.post('/api/generate', {query, k:5});\n        const genMap = {}\n        g.data.results.forEach(r=>genMap[r.uniq_id || r.title]=r.generated_description)\n        setResults(prev => prev.map(p=>({...p, generated_description: genMap[p.uniq_id || p.title]})))\n      }catch(e){console.error('gen error',e)}finally{setGenLoading(false)}
    }catch(err){
      console.error(err);
    }
  }

  return (
    <div className="container">
      <h1>Product Recommendation (Demo)</h1>
      <p className="note">This React app talks to the FastAPI backend. Start backend first.</p>
      <form onSubmit={handleSearch} className="searchForm">
        <input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Type a product query, e.g., 'leather shoes'"/>
        <button type="submit">Recommend</button>
      </form>
      {summary && <div className="summary">Dataset: {summary.num_items} items • {summary.num_categories} categories • avg price {summary.avg_price.toFixed(2)}</div>}
      <div className="results">
        {results.map((r,i)=>(
          <div className="card" key={i}>
            <img src={r.image || 'https://via.placeholder.com/150'} alt={r.title} onError={(e)=>e.target.src='https://via.placeholder.com/150'} />
            <div className="info">
              <h3>{r.title}</h3>
              <div className="meta">{r.brand} • {r.category} • ${r.price}</div>
              <div className="score">Score: {r.score.toFixed(2)}</div>\n              <div className="gen">{r.generated_description || (genLoading? 'Generating...':'No description')}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
