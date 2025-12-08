import axios, { AxiosResponse } from 'axios';
import https from 'https';


export default async function callSramForUserLogin(user: string, service: string): Promise<AxiosResponse<any, any, {}> | null> {
  const agent = new https.Agent({ rejectUnauthorized: false });
  
    let response = null;
  
    try {
      response = await axios.post('https://sbs.scz-vm.net/api/users/proxy_authz', {
        user_id: user,
        service_id: service,
        issuer_id: 'issuer.com',
      }, {
        headers: {
          // Use username and password as defined in environments/vm/secrets/all.yml
          'Authorization': 'Basic ' + Buffer.from('sysadmin:changethispassword').toString('base64')
        },
        httpsAgent: agent
      });
    } catch(error) {
      console.error('Error during API request:', error);
    }
    return response;
}