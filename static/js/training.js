var refresher = setInterval(refresh, 15000);
$('.section-profile').bind('destroyed', function() {
    clearInterval(refresher);
});
$(document).ready(function () {
    refresh();
});

var layerFileData = {};

var certificate;

function loadCertification(){
    function loadCert(data){
        data[0].badges.forEach(function(badge) {
            let template = $("#badge-template").clone();
            template.attr("id", "badge-" + badge.name);
            template.find('#badge-name').text(badge.name);
            template.find('#badge-icon').attr('src', '/training/img/badges/'+badge.name+'.png');
            template.show();
            $('#badges').append(template);
        });
        refresh();
    }
    let selectedCert = $('#certification-name option:selected').attr('value');
    stream('Hover over each flag to get adversary emulation tips & tricks!');
    certificate = certificates.find(function(cert){ return cert.name == selectedCert});
    setCertDescription();
    setCertRefresh();
    $('#badges').empty();
    restRequest('POST', {"index":"certifications","name":selectedCert}, loadCert)
}

function setCertDescription() {
    $('#training-cert-description-modal').find('h3').text(certificate.name);
    $('#training-cert-description-modal').find('p').html(certificate.description);
}

function setCertRefresh() {
    if (certificate.cert_type && certificate.cert_type == "exam") {
        clearInterval(refresher);
        $("#btn-check-answers").show();
    }
    else {
        $("#btn-check-answers").hide();
        refresher = setInterval(refresh, 15000);
    }
}

function refresh(){
    let selectedCert = $('#certification-name option:selected').attr('value');
    if(!selectedCert){
        return;
    }
    $('#training-disclaimers').hide();
    restRequest('POST', {"name":selectedCert, "answers":[]}, update, '/plugin/training/flags')
}

function update(data){
    let completedBadges = 0;
    let code = [];
    let flags = $('#flags');
    flags.empty();

    badgeLoop:
    for (var badgeIdx in data.badges) {
        var badge = data.badges[badgeIdx];
        let badgeComplete = 0;
        let b = $('#badge-'+badge.name);
        b.find('.badge-icon').addClass('badge-in-progress');
        b.attr('status', 'progress');
        for (var flagIdx in badge.flags) {
            var flag = badge.flags[flagIdx];
            let flagHTML = createFlagHTML(badge, flag);
            if(flag.completed) {
                flagHTML.find('#flag-status').html('&#x2705;');
                flagHTML.find("input").attr("disabled", true);
                flagHTML.find("button").removeClass("button-success").attr("disabled", true);
                badgeComplete += 1;
                code.push(flag.code);
                flags.append(flagHTML);
            } else {
                flagHTML.find('#flag-status').html('&#10060;');
                if (flag.resettable === 'True') {
                    flagHTML.find('.flag-reset-button').show();
                }
                flags.append(flagHTML);
                if (!certificate.cert_type) {
                    break badgeLoop; //show only the next incomplete flag
                }
            }
        }
        if(badgeComplete === badge.flags.length) {
            b.find('.badge-icon').removeClass('badge-in-progress');
            b.find('.badge-icon').addClass('badge-completed');
            b.attr('status', 'completed');
            completedBadges += 1
        }
    }
    showRelevantFlags();
    displayCert(code, completedBadges, data.badges.length);
}

function createFlagHTML(badge, flag) {
    let template = $("#flag-template").clone();
    template.removeAttr('id');
    template.attr('badge', badge.name);
    template.find('#flag-number').html('&#127937 ' + flag.number);
    template.find('#flag-name').text(flag.name);
    template.find("#flag-challenge").text(flag.challenge);
    if (flag.flag_type) {
        addAnswerOptions(flag, template);
    }
    if (flag.extra_info == null || flag.extra_info == "") {
        template.find(".flip-card-inner").attr('data-flip', 'false');
    } else {
        template.find("#flag-info").text(flag.extra_info);
    }
    template.find("#flag-completed-ts").text(flag.completed_timestamp);
    return template
}

function addAnswerOptions(flag, template) {
    template.find("#flag-answer").show();
    template.find("#flag-answer").attr("id", "flag-answer-" + flag.number);
    template.find("#flag-answer-" + flag.number).addClass("flag-answer");
    template.find("#flag-answer-" + flag.number).addClass(flag.flag_type);
    switch (flag.flag_type) {
        case "multiplechoice":
            let mcType = flag.multi_select ? 'checkbox' : 'radio'
            flag.options.forEach(function(o) {
                let btnSet = "mult-" + flag.number;
                let radioHTML = "<label><input type='" + mcType + "' name='" + btnSet + "' value='" + o + "'>" + o + "</label><br>";
                template.find("#flag-answer-" + flag.number).append(radioHTML);
            })
            break;
        case "fillinblank":
            template.find("#flag-answer-" + flag.number).append("<input class='fill-in-the-blank'>");
            break;
        case "navigator":
            let uploadHTML = "<input id='layer-upload' class='layer-upload' type='file' accept='.json' hidden>" +
                        "<button class='button-success atomic-button' onclick='uploadLayer(this)'>Upload Layer</button>" +
                        "<p id='layer-upload-filename' style='margin:0px; padding:10px 0px;'></p>";
            template.find("#flag-answer-" + flag.number).append(uploadHTML);
            break;
        default:
            stream("Unknown flag type provided");
    }
}

function showRelevantFlags() {
    let flags = $('#flags');
    let selected = $('#badges').find('.selected-badge');
    if (selected.length) {
        var badge_name = selected.find('#badge-name').text();
        flags.find('li').each(function() {
            if ($(this).attr('badge') === badge_name) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    } else {
        flags.find('li').each(function() {
            $(this).show();
        });
    }
}

function getAnswers() {
    let answers = {}
    $(".flag-answer").each(function(i, set) {
        if ($(set).parent().find("#flag-status").html().charCodeAt(0) == 9989) {
//        skip flags that have already been completed
            return;
        }
        let flagNum = $(set).attr("id").split("-")[2];
        let type = $(set).attr("class").split(" ")[1];
        let answer = [];

        switch (type) {
            case "multiplechoice":
                answer = $(set).find("input:checked");
                if (answer.length > 1) {
        //        multiselect multiple choice
                    let arr = [];
                    answer.each(function(idx, a) {
                        arr.push(a.value)
                    })
                    answer = arr
                }
                else if (answer.length == 1) {
        //        single option multiple choice
                    answer = answer.val();
                }
                else {
                    answer = "";
                }
                break;
            case "fillinblank":
                answer = $(set).find("input:not([type=checkbox],[type=radio],[type=file])").val();
                break;
            case "navigator":
                answer = layerFileData[flagNum];
                break;
            default:
                stream("Unknown flag type provided");
        }
        answers[flagNum] = answer;
    })
    return answers;
}

function selectBadge(element) {
    if ($(element).hasClass('selected-badge')) {
        $(element).removeAttr('class');
        $(element).find('.badge-icon').removeAttr('id');
        showRelevantFlags();
    } else if ($(element).attr('status')){
        $('#badges').find('li').each(function() {
            $(this).removeAttr('class');
            $(this).find('.badge-icon').removeAttr('id');
        });
        $(element).attr('class', 'selected-badge');
        $(element).find('.badge-icon').attr('id', 'selected-badge-icon');
        showRelevantFlags();
    }
}

function displayCert(code, completedBadges, totalBadges) {
    if(completedBadges === totalBadges) {
        code = code.sort(function(a, b) {
            return a.toString().length - b.toString().length;
        });
        code = code.join(' ');
        document.getElementById("alert-modal").style.display="block";
        let alert_text = "Congratulations! You've completed the certification! The code for the certification is below:\n\n" + btoa(code);
        $('#alert-text').html(alert_text).css('white-space', 'pre-wrap');
        $('#alert-text').html(alert_text).css('word-wrap', 'break-word');
        clearInterval(refresher);
    }
}

function checkAnswers() {
    let answers = allAnswered();
    if (answers) {
        let selectedCert = $('#certification-name option:selected').attr('value');
        restRequest('POST', {"name":selectedCert, "answers":answers}, update, '/plugin/training/flags');
    }
}

function allAnswered() {
    let answers = getAnswers()

    let complete = true
    for (var a in answers) {
        complete = complete && answers[a];
    }
    if (complete || confirm("There are still unanswered questions, are you absolutely sure you want to submit?")) {
        return answers
    }
    else {
        return null
    }
}

function uploadLayer(btn) {
    $(btn).siblings("#layer-upload").click();
}

$("body").on("change", "input.layer-upload", async function (event){
    if(event.currentTarget) {
        let file = event.currentTarget.files[0];
        let parentId = $(this).parent().attr("id").split("-")[2];
        if(file && file.name){
            $(this).siblings("#layer-upload-filename").html(file.name);
            try {
                layerFileData[parentId] = await readUploadedFileAsText(file)
            } catch (e) {
                console.warn(e.message)
            }
        }
        else {
            $(this).siblings("#layer-upload-filename").html("");
            delete layerFileData[parentId];
        }
    }
});

function readUploadedFileAsText(inputFile) {
    const temporaryFileReader = new FileReader();

    return new Promise((resolve, reject) => {
        temporaryFileReader.onerror = () => {
            temporaryFileReader.abort();
            reject(new DOMException("Problem parsing input file."));
        };

        temporaryFileReader.onload = () => {
            resolve(temporaryFileReader.result);
        };
        temporaryFileReader.readAsText(inputFile);
  });
}

function trainingSendFlagReset() {
    let selectedCert = $('#certification-name option:selected').attr('value');
    if(!selectedCert){
        return;
    }
    restRequest('POST', {"name":selectedCert}, resetCallback, '/plugin/training/reset_flag');
}

function resetCallback(data) {
    if (data.reset === 1) {
        stream('The flag has been reset.');
    } else {
        stream('The flag cannot be reset.');
    }
}
