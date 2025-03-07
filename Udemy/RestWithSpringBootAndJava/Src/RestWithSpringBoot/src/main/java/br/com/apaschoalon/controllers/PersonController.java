package br.com.apaschoalon.controllers;

import java.util.List;
import java.util.logging.Logger;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import br.com.apaschoalon.data.vo.v1.PersonVO;
import br.com.apaschoalon.services.PersonServices;
import br.com.apaschoalon.util.MediaType;
//import org.springframework.http.MediaType;


@RestController
@RequestMapping("/person")
public class PersonController {

	
	private Logger logger = Logger.getLogger(PersonController.class.getName());
	
	@Autowired
	private PersonServices service;
	
	@GetMapping(value="/{id}",
			produces = {MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML, MediaType.APPLICATION_YML})
	public PersonVO findById(
			@PathVariable(value="id") Long id){
		return this.service.findById(id);
	}

	@GetMapping(
			produces = {MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML, MediaType.APPLICATION_YML})
	public List<PersonVO> findAll(){
		var all = this.service.findAll();
		this.logger.info("all.size():" + all.size());
		return all;
	}
	
	@PostMapping(
			consumes = {MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML, MediaType.APPLICATION_YML},
			produces = {MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML, MediaType.APPLICATION_YML})
	public PersonVO create(
			@RequestBody PersonVO person){
		return this.service.create(person);
	}	
	
	
	@PutMapping(
			consumes = {MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML, MediaType.APPLICATION_YML},
			produces = {MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML, MediaType.APPLICATION_YML})
	public PersonVO update(
			@RequestBody PersonVO person){
		return this.service.update(person);
	}		
	
	@DeleteMapping(value="/{id}")
	public ResponseEntity<?> delete(
			@PathVariable(value="id") Long id){
		this.service.delete(id);
		return ResponseEntity.noContent().build();
	}	
	
}
