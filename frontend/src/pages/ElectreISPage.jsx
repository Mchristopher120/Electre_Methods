import React, {useState} from 'react'
import axios from 'axios'
import { Button, Box, Typography } from '@mui/material'
import MatrixEditor from '../components/MatrixEditor'
import ParamInputs from '../components/ParamInputs'
import ResultsTable from '../components/ResultsTable'
import GraphViewCytoscape from '../components/GraphViewCytoscape'

export default function ElectreISPage(){
  const [criteria, setCriteria] = useState(2)
  const [alternatives, setAlternatives] = useState(2)
  const [matrix, setMatrix] = useState(Array.from({length:2},()=>Array.from({length:2},()=>'')))
  const [weights, setWeights] = useState([ '', '' ])
  const [p, setP] = useState(Array.from({length:2},()=>''))
  const [q, setQ] = useState(Array.from({length:2},()=>''))
  const [v, setV] = useState(Array.from({length:2},()=>''))
  const [params, setParams] = useState({ei_s_lambda: '0.5', maximum_cycles: '15'})
  const [result, setResult] = useState([])
  const [graphPayload, setGraphPayload] = useState({ performance: [], weights: [], p: [], q: [], v: [] })

  const callSolve = async () => {
    const perf = matrix.map(r => r.map(vv => parseFloat(vv || '0')))
    const body = { performance: perf, weights: weights.map(x=>parseFloat(x||'0')), p: p.map(x=>parseFloat(x||'0')), q: q.map(x=>parseFloat(x||'0')), v: v.map(x=>parseFloat(x||'0')), ei_s_lambda: parseFloat(params.ei_s_lambda), maximum_cycles: parseInt(params.maximum_cycles) }
    const res = await axios.post('/electre/i_s', body)
    setResult(res.data.result)
    setGraphPayload(body)
  }

  return (
    <Box>
      <Typography variant="h5">ELECTRE I_s</Typography>
      <ParamInputs params={{criteria, alternatives, ...params}} onChange={p2 => {if(p2.criteria) setCriteria(parseInt(p2.criteria)); if(p2.alternatives) setAlternatives(parseInt(p2.alternatives)); setParams({ei_s_lambda: p2.ei_s_lambda ?? params.ei_s_lambda, maximum_cycles: p2.maximum_cycles ?? params.maximum_cycles})}} />
      <Typography>Top parameter rows: q (row0), p (row1), v (row2), W weights (row3)</Typography>
      <MatrixEditor rows={4} cols={criteria} value={[q,p,v,weights]} onChange={([r0,r1,r2,r3]) => { setQ(r0); setP(r1); setV(r2); setWeights(r3) }} />
      <Typography>Performance matrix (alternatives x criteria):</Typography>
      <MatrixEditor rows={alternatives} cols={criteria} value={matrix} onChange={setMatrix} />
      <Box sx={{my:2}}>
        <Button variant="contained" onClick={callSolve}>Solve</Button>
      </Box>
      <Typography>Results:</Typography>
      <ResultsTable data={result} />
    </Box>
  )
}
