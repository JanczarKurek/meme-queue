import React from 'react'
import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

class FoodBar extends React.Component {
    DUŻO = 2
    MAŁO = 1
    NIC = 0
    status_to_value = {
        "ser": {
            "Otóż TAK!!!": this.DUŻO,
            "Już prawie nie ma, @Piotr kup ser": this.MAŁO,
            "SER SIĘ SKOŃCZYŁ!!!!!!!!!!!!1111111jedenjeden": this.NIC,
        },
        "chleb": {
            "Otóż TAK!!!": this.DUŻO,
            "Już prawie nie ma": this.MAŁO,
            "GŁODÓWKA NIE MA TOSTÓW!!!!!!!!!!!!1111111jedenjeden": this.NIC,
        },
        "mleko": {
            "Otóż TAK!!!": this.DUŻO,
            "Już prawie nie ma": this.MAŁO,
            "JEMY PŁATKI Z KAWĄ!!!!!!!!!!!!1111111jedenjeden": this.NIC,
        },
    }
    value_to_pos = {
        "ser": 0, "chleb": 1, "mleko": 2,
    }
    constructor(props) {
        super(props);
        this.state = {
            data: {
                labels: [""],
                datasets: [
                    {
                        label: 'ser',
                        data: [0],
                        backgroundColor: 'red',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    },
                    {
                        label: 'chleb',
                        data: [1],
                        backgroundColor: 'green',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    },
                    {
                        label: 'mleko',
                        data: [2],
                        backgroundColor: 'blue',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Stan jedzenia',
                    },
                },
            },
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.events === this.props.events || !this.props.events)
            return;


        let newState = structuredClone(this.state)
        for (let event of this.props.events) {
            if (event.resource_tag === "status") {
                for (let [food, status] of Object.entries(event.payload)) {
                    newState.data.datasets[this.value_to_pos[food]].data = [this.status_to_value[food][status]]
                }
                this.setState(newState)
            }
        }
    }

    render() {
        if (this.props.visible)
            return <Bar data={this.state.data} options={this.state.options} />;
        else
            return (<div></div>)
    }

}

export default FoodBar;