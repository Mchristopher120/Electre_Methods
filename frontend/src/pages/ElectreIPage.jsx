import React, {useState} from 'react'
import axios from 'axios'
import { Button, Box, Typography } from '@mui/material'
import MatrixEditor from '../components/MatrixEditor'
import ParamInputs from '../components/ParamInputs'
import ResultsTable from '../components/ResultsTable'
import GraphViewCytoscape from '../components/GraphViewCytoscape'

export default function ElectreIPage(){
  const [criteria, setCriteria] = useState(2)
  const [alternatives, setAlternatives] = useState(2)
  const [matrix, setMatrix] = useState(Array.from({length:2},()=>Array.from({length:2},()=>'')))
  const [weights, setWeights] = useState([ '', '' ])
  const [params, setParams] = useState({ei_p: '0.0', ei_q: '0.0'})
  const [result, setResult] = useState([])
  const [graphPayload, setGraphPayload] = useState({ performance: [], weights: [], ei_p: 0.0, ei_q: 0.0 })

  const callSolve = async () => {
    // assemble payload
    const perf = matrix.map(r => r.map(v => parseFloat(v || '0')))
    const w = weights.map(v => parseFloat(v || '0'))
    const body = { performance: perf, weights: w, ei_p: parseFloat(params.ei_p), ei_q: parseFloat(params.ei_q) }
    const res = await axios.post('/electre/i', body)
    setResult(res.data.result)
    setGraphPayload(body)
    // fetch graph data and show? we could show graph below
  }

  return (
    <Box>
      <Typography variant="h5">ELECTRE I</Typography>
      <Box sx={{my:2}}>
        <ParamInputs params={{criteria, alternatives, ...params}} onChange={p => {if(p.criteria) setCriteria(parseInt(p.criteria)); if(p.alternatives) setAlternatives(parseInt(p.alternatives)); setParams({ei_p: p.ei_p ?? params.ei_p, ei_q: p.ei_q ?? params.ei_q})}} />
      </Box>
      <Typography>Weights (one row):</Typography>
      <MatrixEditor rows={1} cols={criteria} value={[weights]} onChange={v => setWeights(v[0])} />
      <Typography>Performance matrix (alternatives x criteria):</Typography>
      <MatrixEditor rows={alternatives} cols={criteria} value={matrix} onChange={setMatrix} />
      <Box sx={{my:2}}>
        <Button variant="contained" onClick={callSolve}>Solve</Button>
      </Box>
      <Typography>Results:</Typography>
      <ResultsTable data={result} />
      <Typography sx={{mt:2}}>Graph:</Typography>
      {/* Graph view uses graph/data/ei endpoint */}
      <div style={{marginTop:8}}>
        <GraphViewCytoscape method={'ei'} payload={graphPayload} />
      </div>
    </Box>
  )
}
