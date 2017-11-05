import React from 'react';
import PropTypes from 'prop-types';

import {Table} from 'react-bootstrap';


const ToiletEntries = (props) => {
  return (
    <Table>
      <thead>
        <tr>
          <th>Toilet #</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>{props.children}</tbody>
    </Table>
  );
};

export default ToiletEntries;
