//Variables
var express = require('express');
var app = express();
app.use(express.json());

// Diccionario 
var jedis = [
    {name: 'Yoda', id: 1},
    {name: 'Luke', id: 2},
    {name: 'Obi wan', id: 3}
];

app.get('/', (req, res) => {
    res.send('Jedi REST api');
});

// Crear un webserver en el puerto 66   
app.listen(66, () => console.log("Listening on port "));


// Query all jedis
// GET
app.get('/api/jedis', (req,res)=> {
    res.json(jedis);
});

// Just one jedi
// GET
app.get('/api/jedis/:id', (req, res) => {
    const jedi = jedis.find(c => c.id === parseInt(req.params.id));
    if (!jedi) res.status(404).send('Not found');
    res.json(jedi);
});

// Create Jedi
// POST
app.post('/api/jedis', (req, res)=> {
    var jedi = {
        id: jedis.length + 1,
        name: req.body.name
    };
    console.log(jedi);
    jedis.push(jedi);
    res.json(jedi);
});

// Modify Jedi
// PUT
app.put('/api/jedis/:id', (req, res) => {
    var jedi = jedis.find(c=> c.id === parseInt(req.params.id));
    if (!jedi) res.status(404).send('Not found');
    jedi.name = req.body.name;
    res.json(jedi);
});

// Delete Jedi
// Delete
app.delete('/api/jedis/:id', (req, res) => {
    var jedi = jedis.find( c=> c.id === parseInt(req.params.id));
    if (!jedi) res.status(404).send('Not found');
    var index = jedis.indexOf(jedi);
    jedis.splice(index,1);
    res.json(jedi);
});


