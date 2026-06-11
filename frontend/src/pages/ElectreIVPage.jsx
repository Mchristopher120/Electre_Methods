import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Button, Box, Typography } from '@mui/material'
import MatrixEditor from '../components/MatrixEditor'
import ParamInputs from '../components/ParamInputs'
import ResultsTable from '../components/ResultsTable'
import GraphViewCytoscape from '../components/GraphViewCytoscape'
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, LabelList } from 'recharts'
import Heatmap from '../components/Heatmap'

export default function ElectreIVPage(){
  const [criteria, setCriteria] = useState(2)
  const [alternatives, setAlternatives] = useState(2)
  const [matrix, setMatrix] = useState(Array.from({length:2},()=>Array.from({length:2},()=>'')))
  const [p, setP] = useState(Array.from({length:2},()=>''))
  const [q, setQ] = useState(Array.from({length:2},()=>''))
  const [v, setV] = useState(Array.from({length:2},()=>''))
  const [result, setResult] = useState([])
  const [graphPayload, setGraphPayload] = useState({ performance: [], p: [], q: [], v: [] })
  const [rankingData, setRankingData] = useState([])
  const [credibilityMatrix, setCredibilityMatrix] = useState(null)

  const callSolve = async () => {
    const perf = matrix.map(r => r.map(vv => parseFloat(vv || '0')))
    const body = { performance: perf, p: p.map(x=>parseFloat(x||'0')), q: q.map(x=>parseFloat(x||'0')), v: v.map(x=>parseFloat(x||'0')) }
    const res = await axios.post('/electre/iv', body)
    setResult(res.data.result)
    setGraphPayload(body)
  }

  useEffect(()=>{
    async function fetchRanking(){
      if(!graphPayload || !graphPayload.performance || graphPayload.performance.length === 0) return
      try{
        const res = await axios.post('/graph/data/iv', graphPayload)
        const ranks = res.data.rankings || []
        setCredibilityMatrix(res.data.credibility || null)
        const data = ranks.map(r => ({ alt: r.alt, avg: r.avg ?? r.value ?? null }))
        data.sort((a,b)=> (b.avg ?? 0) - (a.avg ?? 0))
        setRankingData(data)
      }catch(err){ console.error(err) }
    }
    fetchRanking()
  },[graphPayload])

  return (
    <Box>
      <Typography variant="h5">ELECTRE I_v / IV (shared page)</Typography>
      <ParamInputs params={{criteria, alternatives}} onChange={p2 => { if(p2.criteria) setCriteria(parseInt(p2.criteria)); if(p2.alternatives) setAlternatives(parseInt(p2.alternatives))}} />
      <Typography>Top parameter rows: q (row0), p (row1), v (row2)</Typography>
      <MatrixEditor rows={3} cols={criteria} value={[q,p,v]} onChange={([r0,r1,r2]) => { setQ(r0); setP(r1); setV(r2) }} />
      <Typography>Performance matrix (alternatives x criteria):</Typography>
      <MatrixEditor rows={alternatives} cols={criteria} value={matrix} onChange={setMatrix} />
      <Box sx={{my:2}}>
        <Button variant="contained" onClick={callSolve}>Solve (ELECTRE IV)</Button>
      </Box>
      <Typography>Results:</Typography>
      <ResultsTable data={result} />
      <Typography sx={{mt:2}}>Graph:</Typography>
      <div style={{marginTop:8}}>
        <GraphViewCytoscape method={'iv'} payload={graphPayload} />
      </div>
      <Typography sx={{mt:2}}>Credibility heatmap:</Typography>
      <div style={{marginTop:8}}>
        <Heatmap matrix={credibilityMatrix} />
      </div>
      <Typography sx={{mt:2}}>Ranking (average):</Typography>
      <div style={{marginTop:8}}>
        <BarChart width={600} height={300} data={rankingData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="alt" type="category" />
          <Tooltip />
          <Bar dataKey="avg" fill="#ffc658">
            <LabelList dataKey="avg" position="right" />
          </Bar>
        </BarChart>
      </div>
    </Box>
  )
}
