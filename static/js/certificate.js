function downloadCertificate(endpoint='/plugin/training/certificate', data={}) {
	let name = $('#cert-name').val();
	function downloadObjectAsJson(data){
		let bytes = b64ToByteArray(data['img']);
		let blob = new Blob([bytes], {type: 'image/jpeg'});
		let filename = name + ' - Certificate';
		stream('Downloading certificate: '+filename);
		downloadCert(blob, filename);
	}

	function b64ToByteArray(blob) {
		let binStr = atob(blob);
		let binLen = binStr.length;
		let bytes = new Uint8Array(binLen);
		for (let i = 0; i < binLen; i++) {
			bytes[i] = binStr.charCodeAt(i);
		}
		return bytes;
	}

	function downloadCert(blob, filename) {
		let downloadAnchorNode = document.createElement('a');
		let url = window.URL.createObjectURL(blob);
		downloadAnchorNode.setAttribute("href", url);
		downloadAnchorNode.setAttribute("download", filename + ".jpg");
		document.body.appendChild(downloadAnchorNode);
		downloadAnchorNode.click();
		downloadAnchorNode.remove();
		window.URL.revokeObjectURL(url);
	}

	data['name'] = name;
	data['certification'] = $('#certification-name option:selected').attr('value');;
	restRequest('POST', data, downloadObjectAsJson, endpoint);
}

function downloadBlock() {
	let flags = $('#flags');
	let template = $("#flag-template").clone();
	template.find('#flag-number').html('&#127937');
	template.find('#flag-name').text('CERTIFICATE');
	template.find("#flag-challenge").html('You have successfully completed all flags, your certificate is now available.\n');
	template.find("#flag-info").html(
		'Enter your name for the certificate and click download to receive your red operator certification:' +
		'<input id="cert-name" name="name" type="text" placeholder="Your Name"/>\n' +
		'<input type="button" style="width: 100%;height: 30px;padding: 0;" onclick="downloadCertificate()" value="Download"/>'
	);
	template.find('#flag-status').html('&#11015;');
	template.show();
	template.addClass('completed-training');
	flags.append(template);
}

function getFlagCount(data) {
	let count = 0;
	data.badges.forEach(function(badge) {
		for(let f in badge.flags) {
			count++;
		}
	});
	return count
}

//# sourceURL=certificate.js