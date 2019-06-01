import moment from 'moment';

const CalendarDay = props => (
    <ul className="day {dayNo}">
        <li key="header" className="header">{ moment().isSame(props.day, 'day') ? 'Today' : moment(props.day).format('dddd, Do MMMM') }</li>
        {
            props.events.map(ev => {
                if (ev == false) {
                    return '';
                }

                // Get some usable date objects
                ev.start = moment(ev.start);
                ev.end = moment(ev.end);

                // Check this event is for today
                if (ev.start.isAfter(props.day, 'day') || ev.end.isBefore(props.day, 'day')) {
                    return '';
                }

                let title = ev.start.format('h:mm');
                let subtitle = ev.start.format('a');

                // If started before today
                if (ev.start.isBefore(props.day, 'day')) {
                    title = '';
                    subtitle = 'Continues';
                // If a whole day event
                } else if (ev.start.format('HHmm') == '0000' && ev.end.format('HHmm') == '0000') {
                    title = '';
                    subtitle = 'All day';
                }

                // Style past events differently
                let eclass = '';
                if (moment() > ev.start) {
                    eclass = 'past';
                }

                return (
            <li key={ ev.id } className={ eclass+' cal-'+ev.calendar }>
                <strong>
                    { title }
                    <span>{ subtitle }</span>
                </strong>
                <span>
                    { ev.description }
                </span>
            </li>
                )
            })
        }
    </ul>
)

export default CalendarDay
