package br.com.apaschoalon.services;

import java.util.List;
import java.util.logging.Logger;

import org.hibernate.ResourceClosedException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.linkTo;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.methodOn;

import br.com.apaschoalon.controllers.PersonController;
import br.com.apaschoalon.data.vo.v1.PersonVO;
import br.com.apaschoalon.data.vo.v2.PersonVOV2;
import br.com.apaschoalon.exceptions.RequiredObjectIsNullException;
import br.com.apaschoalon.mapper.DozerMapper;
import br.com.apaschoalon.mapper.custom.PersonMapper;
import br.com.apaschoalon.model.Person;
import br.com.apaschoalon.repositories.PersonRepository;

@Service
public class PersonServices {

	// private final AtomicLong counter = new AtomicLong();
	
	private Logger logger = Logger.getLogger(PersonServices.class.getName());
	
	@Autowired
	PersonRepository repository;
	
	@Autowired
	PersonMapper mapper;
	
	public PersonVO findById(Long id) {
		logger.info("Finding one person...");
		var entity = this.repository.findById(id)
				.orElseThrow(() -> new ResourceClosedException("No records found for this ID: " + id));
		// return DozerMapper.parseObject(entity, PersonVO.class);
		var vo =  DozerMapper.parseObject(entity, PersonVO.class);
		vo.add(linkTo(methodOn(PersonController.class).findById(id)).withSelfRel());
		return vo;
	}
	
	public List<PersonVO> findAll() {
		logger.info("Finding all people...");
		var persons = DozerMapper.parseListObjects(this.repository.findAll(), PersonVO.class);
		persons
			.stream()
			.forEach(p -> p.add(linkTo(methodOn(PersonController.class).findById(p.getKey())).withSelfRel()));
		return persons;
	}

	public PersonVO create(PersonVO person) {
		if(person == null) 
		{
			throw new RequiredObjectIsNullException();
		}
		
		logger.info("Creating one person!");
		var entity = DozerMapper.parseObject(person, Person.class);
		
		var savedPerson  = this.repository.save(entity);
		var vo = DozerMapper.parseObject(savedPerson, PersonVO.class);
		vo.add(linkTo(methodOn(PersonController.class).findById(vo.getKey())).withSelfRel());
		return vo;
	}	
	
	public PersonVOV2 createV2(PersonVOV2 person) {
		logger.info("Creating one person v2!");
		var entity = this.mapper.convertVOV2ToEntity(person);
		
		var savedPerson  = this.repository.save(entity);
		var vo = this.mapper.convertEntityToVoV2(savedPerson);
		return vo;
	}		
	

	public PersonVO update(PersonVO person) {
		if(person == null) 
		{
			throw new RequiredObjectIsNullException();
		}
		
		logger.info("Creating one person!");
		
		var entity = this.repository.findById(person.getKey())
				.orElseThrow(() -> new ResourceClosedException("No records found for this ID: " + person.getKey()));
		
		entity.setFirstName(person.getFirstName());
		entity.setLastName(person.getLastName());
		entity.setAddress(person.getAddress());
		entity.setGender(person.getGender());		
		
		var savedPerson  = this.repository.save(entity);
		var vo = DozerMapper.parseObject(savedPerson, PersonVO.class);
		vo.add(linkTo(methodOn(PersonController.class).findById(vo.getKey())).withSelfRel());
		return vo;
	}	
	
	public void delete(Long id) {
		logger.info("Deleting one person!");
		var entity = this.repository.findById(id)
				.orElseThrow(() -> new ResourceClosedException("No records found for this ID: " + id));
		this.repository.delete(entity);
	}	
	
	// private Person mockPerson(int i) {
	// 
	// 	Person person = new Person();
	// 	person.setId(this.counter.getAndIncrement());
	// 	person.setFirstName("Person Name " + i);
	// 	person.setLastName("Last Name " + i);
	// 	person.setAddress("Adress " + i);
	// 	person.setGender("Male");
	// 	
	// 	return person;
	// }	


	
}
